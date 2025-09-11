<script setup lang="ts">
import { ref, watch } from "vue";
import {useRouter} from "vue-router";
import * as yup from "yup";
import { useField, useForm } from "vee-validate";
import {useUser} from "@/stores/User";
import { stubDocumentsIcon} from "@/assets/icons";
import { AppColors } from "@/enums/appColors.ts";

const router = useRouter()
const userStore = useUser()


const previewIcons = [ref<string | undefined>(stubDocumentsIcon), ref<string | undefined>(stubDocumentsIcon), ref<string | undefined>(stubDocumentsIcon), ref<string | undefined>(stubDocumentsIcon)];
const fileInputs = [
  ref<HTMLInputElement | null>(null),
  ref<HTMLInputElement | null>(null),
  ref<HTMLInputElement | null>(null),
  ref<HTMLInputElement | null>(null)
];

const { handleSubmit, validate, errors } = useForm({
  validationSchema: yup.object({
    checkboxPersonal: yup.boolean().oneOf([true]).required(),
    checkboxTrueData: yup.boolean().oneOf([true]).required(),
    photoFile1: yup.mixed().required('Фото обязательно для загрузки').test('fileType', 'Только изображения (PNG или JPEG)', (value) => {
      return value instanceof File && (value.type === 'image/png' || value.type === 'image/jpeg');
    }),
    photoFile2: yup.mixed().required('Фото обязательно для загрузки').test('fileType', 'Только изображения (PNG или JPEG)', (value) => {
      return value instanceof File && (value.type === 'image/png' || value.type === 'image/jpeg');
    }),
    photoFile3: yup.mixed().required('Фото обязательно для загрузки').test('fileType', 'Только изображения (PNG или JPEG)', (value) => {
      return value instanceof File && (value.type === 'image/png' || value.type === 'image/jpeg');
    }),
    photoFile4: yup.mixed().required('Фото обязательно для загрузки').test('fileType', 'Только изображения (PNG или JPEG)', (value) => {
      return value instanceof File && (value.type === 'image/png' || value.type === 'image/jpeg');
    })
  }),
});

const isFormValid = ref(false)
const isSetError = ref(false);
const isLoading = ref(false)

const photoFile1 = useField<File>('photoFile1');
const photoFile2 = useField<File>('photoFile2');
const photoFile3 = useField<File>('photoFile3');
const photoFile4 = useField<File>('photoFile4');
const checkboxPersonal = useField('checkboxPersonal');
const checkboxTrueData = useField('checkboxTrueData');

const triggerFileInput = (index: number) => {
  const inputArray = fileInputs[index].value;
  if (Array.isArray(inputArray) && inputArray.length > 0) {
    const inputElement = inputArray[0] as HTMLInputElement;
    inputElement.click();
  } else {
    console.error(`fileInput at index ${index} is not available or empty`);
  }
};

const handleFileChange = (event: Event, index: number) => {
  const target = event.target as HTMLInputElement;
  if (!target.files || target.files.length === 0) return;

  const file = target.files[0];
  previewIcons[index].value = URL.createObjectURL(file); // Создание URL для предпросмотра
  switch (index) {
    case 0:
      photoFile1.value.value = file;
      break;
    case 1:
      photoFile2.value.value = file;
      break;
    case 2:
      photoFile3.value.value = file;
      break;
    case 3:
      photoFile4.value.value = file;
      break;
  }
};

const checkValidity = async () => {
  await validate()
  return Object.keys(errors.value).length === 0
}

const updateValidity = async () => {
  isFormValid.value = await checkValidity()
}

watch([photoFile1.value, photoFile2.value, photoFile3.value, photoFile4.value, checkboxPersonal.value, checkboxTrueData.value], () => {
  updateValidity()
})

const submit = handleSubmit(async (values) => {
  isLoading.value = true;

  const body: any = {
    photoFile1: values.photoFile1,
    photoFile2: values.photoFile2,
    photoFile3: values.photoFile3,
    photoFile4: values.photoFile4,
    checkboxPersonal: values.checkboxPersonal,
    checkboxTrueData: values.checkboxTrueData,
  };
  // console.log(body)
  userStore.setVerifiedStatus(true)
  await router.push("/account")
  try {
    // отправка данных
  } catch (error) {
    console.log("Catch in submit:", error);
    isSetError.value = true;
    const errorMessage = error instanceof Error ? error.message : "Неизвестная ошибка";
    checkboxTrueData.setErrors([errorMessage]);
  } finally {
    isLoading.value = false;
  }
});
</script>



<template>
  <v-container class="verification" fluid>
    <h2 class="title">Верификация учётной записи(Ф)</h2>
    <form @submit.prevent="submit" class=" mt-4">
      <h4 class="lgb">Сканы документов</h4>
      <v-row class="ma-0 pa-0 justify-start align-end gc-8">

        <div v-for="(previewIcon, index) in previewIcons" :key="index" class="d-flex align-center ga-2 position-relative change-photo pa-4 mt-4 mt-sm-2">
          <v-avatar size="72">
            <v-img :src="previewIcon.value ?? ''"></v-img>
          </v-avatar>
          <div class="d-flex justify-center flex-1-1">
            <v-btn variant="text" height="72" class="change-photo-button px-0" @click="triggerFileInput(index)">
              Загрузить
            </v-btn>
            <input type="file" :ref="fileInputs[index]" accept="image/png, image/jpeg" class="d-none"
                   @change="handleFileChange($event, index)" />
          </div>
          <p class="change-photo-description">Тип документа</p>
        </div>

      </v-row>
      <v-row>
        <v-col cols="auto" class="pa-0">
          <v-checkbox
            class="custom-checkbox"
            v-model="checkboxPersonal.value.value"
            label="Я даю согласие на обработку моих персональных данных"
            type="checkbox"
            value="1"
          ></v-checkbox>
          <v-checkbox
            class="custom-checkbox"
            v-model="checkboxTrueData.value.value"
            label="Я подтверждаю, что предоставленные мною данные достоверны и соответствуют ..."
            type="checkbox"
            value="1"
          ></v-checkbox>
        </v-col>
      </v-row>
      <v-row justify="end" class="mt-8">
        <v-col cols="auto">
          <v-btn
            class="mt-6 pa-4 submit-button width-block"
            type="submit"
            height="56"
            rounded="lg"
            :disabled="!isFormValid"
            :base-color="isFormValid ? AppColors.BASE_COLOR_100  : AppColors.BASE_COLOR_40"
            :color="isFormValid ? AppColors.ACCENT_COLOR_LIME_100 : AppColors.ACCENT_COLOR_LIME_20"
          >
            Подтвердить
          </v-btn>
        </v-col>
      </v-row>
    </form>
  </v-container>
</template>

<style scoped>
.verification {
  padding: 40px 112px;

  @media (max-width: 960px) {
    padding: 16px 28px 68px;
  }
}

.title{
  font-size: 32px;
  font-weight: 700;
  line-height: 48px;

  @media (max-width: 600px) {
    font-size: 24px;
    line-height: 32px;
  }
}

.change-photo {
  flex: 1;
  border-radius: 12px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.20));
  margin-bottom: 24px;

  @media (max-width: 1160px) {
    flex: unset;
    width: calc(50% - 16px);
  }

  @media (max-width: 600px) {
    flex: unset;
    width: 100%;
  }
}

.change-photo-button {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px; /* 150% */
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: none;
  text-decoration-thickness: 7.5%; /* 1.2px */
  text-underline-offset: 15%; /* 2.4px */
  text-underline-position: from-font;
  text-transform: none;
}

.change-photo-description {
  position: absolute;
  bottom: -24px;
  left: 12px;
  color: var(--Base-color-60, rgba(54, 57, 64, 0.60));
  font-feature-settings: 'salt' on;
  /* Wireframe Kit/Paragraph Regular */
  font-family: Lato sans-serif;
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: 24px;
}


::v-deep(.v-label.v-field-label) {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
  width: 100%;
}

::v-deep(.v-field__outline) {
  opacity: unset;
  border-color: var(--Base-color-20, rgba(54, 57, 64, 0.20)) !important;
  border-radius: 12px !important;
}

::v-deep(.v-input__details) {
  display: none;
}

.custom-checkbox {
  height: 40px;

  @media (max-width: 600px) {
    height: auto;
  }
}
</style>

