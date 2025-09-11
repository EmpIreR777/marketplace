<script setup lang="ts">
import {computed, ref, watch} from "vue";
import {useRouter} from "vue-router";
import * as yup from "yup";
import {useField, useForm} from "vee-validate";
import {stubDocumentsIcon} from "@/assets/icons";
import {formatDate} from "@/utils/helpers.ts";
import {AppColors} from "@/enums/appColors.ts";
import {useUser} from "@/stores/User";


const router = useRouter()
const userStore = useUser()


const previewIcon = ref<string | undefined>(stubDocumentsIcon);
const fileInput = ref<HTMLInputElement | null>(null);

const { handleSubmit, validate, errors } = useForm({
  validationSchema: yup.object({
    lastName: yup.string().required().min(2),
    firstName: yup.string().required().min(2),
    middleName: yup.string().required().min(2),
    checkboxPersonal: yup.boolean().oneOf([true]).required(),
    checkboxTrueData: yup.boolean().oneOf([true]).required(),
    birthDate: yup.date().required('Дата рождения обязательна').nullable(),
    photoFile: yup.mixed().required('Фото обязательно для загрузки').test('fileType', 'Только изображения (PNG или JPEG)', (value) => {
      return value instanceof File && (value.type === 'image/png' || value.type === 'image/jpeg');
    })
  }),
});

const isFormValid = ref(false)
const isSetError = ref(false);
const isLoading = ref(false)

const lastName = useField<string>('lastName')
const firstName = useField<string>('firstName')
const middleName = useField<string>('middleName')
const birthDate = useField<Date | null>('birthDate');
const checkboxPersonal = useField('checkboxPersonal')
const checkboxTrueData = useField('checkboxTrueData')
const photoFile = useField<File>('photoFile'); // Добавляем поле для файл

const menu = ref<boolean>(false);

const formattedBirthDate = computed({
  get: () => (birthDate.value.value ? formatDate(birthDate.value.value) : ""),
  set: (val) => {
    birthDate.value.value = val ? new Date(val) : null;
  },
});
const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;

  if (!target.files || target.files.length === 0) return;

  const file = target.files[0];
  previewIcon.value = URL.createObjectURL(file); // Создаем объектный URL для предпросмотра
  photoFile.value.value = file;
};

const checkValidity = async () => {
  await validate()
  return Object.keys(errors.value).length === 0
}

const updateValidity = async () => {
  isFormValid.value = await checkValidity()
}

watch([ lastName.value, firstName.value, middleName.value, checkboxPersonal.value, checkboxTrueData.value, birthDate.value, photoFile.value], () => {
  updateValidity()
})

const submit = handleSubmit(async (values) => {
  isLoading.value = true;

  const body: any = {
    lastName: values.lastName,
    firstName: values.firstName,
    middleName: values.middleName,
    checkboxPersonal: values.checkboxPersonal,
    checkboxTrueData: values.checkboxTrueData,
    birthDate: values.birthDate ? formatDate(new Date(values.birthDate)) : null,
    photoFile: values.photoFile,
  };
  // console.log(body)
  userStore.setVerifiedStatus(true)
  await router.push("/account")
  try {

  } catch (error) {
    console.log("Catch in submit:", error);
    isSetError.value = true
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
      <v-row class="mx-0 mt-4 mb-0 mt-sm-0 pa-0 justify-start align-start align-md-end">
        <v-col cols="12" sm="6" md="3" class="pa-0">
          <h4 class="lgb">Фото с документами в руках</h4>
          <div class="d-flex align-center ga-2 position-relative change-photo pa-4 mt-2">
            <v-avatar size="72">
              <v-img :src="previewIcon"></v-img>
            </v-avatar>
            <div class="d-flex justify-center flex-1-1">
              <v-btn variant="text" height="72" class="change-photo-button px-0" @click="triggerFileInput">
                Загрузить
              </v-btn>
              <input type="file" ref="fileInput" accept="image/png, image/jpeg" class="d-none"
                     @change="handleFileChange"/>
            </div>
            <p class="change-photo-description">Паспорт / Загран. паспорт / Водительское удостворение</p>
          </div>
        </v-col>
        <v-col cols="12" sm="6" md="9" class="d-flex flex-wrap gc-8 gr-4 py-o pl-0 pl-sm-8 pr-0">
          <v-text-field
            v-model="lastName.value.value"
            label="Фамилия"
            variant="outlined"
            class="input-item"
          ></v-text-field>
          <v-text-field
            v-model="firstName.value.value"
            label="Имя"
            variant="outlined"
            class="input-item"
          ></v-text-field>
          <v-text-field
            v-model="middleName.value.value"
            label="Отчество"
            variant="outlined"
            class="input-item"
          ></v-text-field>
          <v-menu v-model="menu" transition="scale-transition" offset-y :close-on-content-click="false">
            <template v-slot:activator="{ props }">
              <v-text-field
                v-model="formattedBirthDate"
                label="День рождения"
                variant="outlined"
                class="input-item"
                v-bind="props"
                readonly
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="birthDate.value.value"
            @update:modelValue="(val) => { birthDate.value.value = val; menu = false }"
            ></v-date-picker>
          </v-menu>
        </v-col>

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
  border-radius: 12px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.20));
  margin-bottom: 45px;
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
  bottom: -45px;
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

.input-item {
  color: var(--Base-color-60, rgba(54, 57, 64, 0.60));
  width: calc(50% - 16px);


  @media (max-width: 960px) {
    width: 100%;
  }
}

.input-item {
  input[type="date"]::-webkit-calendar-picker-indicator {
    position: absolute;
    right: 10px; /* Регулируй отступ */
    cursor: pointer;
  }
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
  color: var(--Base-color-100, #363940);
  height: 40px;

  @media (max-width: 600px) {
    height: auto;
  }
}
</style>
