<script setup lang="ts">
import { ref, watch } from "vue";
import {useRouter} from "vue-router";
import * as yup from "yup";
import { useField, useForm } from "vee-validate";
import { AppColors } from "@/enums/appColors.ts";
import {useUser} from "@/stores/User";

const router = useRouter()
const userStore = useUser()



const { handleSubmit, validate, errors } = useForm({
  validationSchema: yup.object({
    checkboxPersonal: yup.boolean().oneOf([true]).required(),
    checkboxTrueData: yup.boolean().oneOf([true]).required(),
  }),
});

const isFormValid = ref(false)
const isSetError = ref(false);
const isLoading = ref(false)

const checkboxPersonal = useField('checkboxPersonal');
const checkboxTrueData = useField('checkboxTrueData');


const checkValidity = async () => {
  await validate()
  return Object.keys(errors.value).length === 0
}

const updateValidity = async () => {
  isFormValid.value = await checkValidity()
}

watch([checkboxPersonal.value, checkboxTrueData.value], () => {
  updateValidity()
})

const submit = handleSubmit(async (values) => {
  isLoading.value = true;

  const body: any = {
    checkboxPersonal: values.checkboxPersonal,
    checkboxTrueData: values.checkboxTrueData,
  };
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
      <h4 class="lgb mb-6">Для верификации требуется подписать документ с помощью цифровой подписи</h4>
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

