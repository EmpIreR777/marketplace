<script setup lang="ts">
import {ref, watch} from "vue";
import * as yup from "yup";
import {useField, useForm} from "vee-validate";
import {useUser} from "@/stores/User";
import {AppColors} from "@/enums/appColors.ts";

const userStore = useUser()

const emit = defineEmits<{
  (event: 'change-email', value: boolean): void;
}>();

const {handleSubmit, validate, errors} = useForm({
  validationSchema: yup.object({
    password: yup.string().required().min(2),
    emailNew: yup.string().required().email(),
  }),
})

const password = useField<string>('password')
const emailNew = useField<string>('emailNew')
const visible = ref(false)
const isFormValid = ref(false)
const isLoading = ref(false);
const isSetError = ref(false);

const checkValidity = async () => {
  await validate()
  return Object.keys(errors.value).length === 0
}

const updateValidity = async () => {
  isFormValid.value = await checkValidity()
}

watch([password.value, emailNew.value], () => {
  updateValidity()
})

const submit = handleSubmit(async (values) => {
  // console.log({password: values.password, new_email: values.emailNew})
  isLoading.value = true;
  try {
    await userStore.setEmail({password: values.password, new_email: values.emailNew})
    localStorage.setItem("new_email", values.emailNew);
    emit("change-email", false)
  } catch (error) {
    console.log("Catch in submit:", error);
    isSetError.value = true;
    const errorMessage = error instanceof Error ? error.message : "Неизвестная ошибка";
    emailNew.setErrors([errorMessage]);
  } finally {
    isLoading.value = false;
  }
})
</script>

<template>
  <v-row align="center" justify="center" class="pa-0 ">
    <v-col class="ma-0 change-email-block d-flex flex-column ga-10 justify-between" cols="auto">
      <div>
        <h5 class="title text-center align-center justify-center">Смена email</h5>
        <p class="sub-title text-center mt-4">Текущий email будет отвязан</p>
      </div>


      <form @submit.prevent="submit">
        <v-text-field
            class="input-block"
            variant="outlined"
            v-model="emailNew.value.value"
            label="Новый Email"
            rounded="lg"
            :error-messages="isSetError? emailNew.errorMessage.value:''"
        ></v-text-field>
        <v-text-field
          :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
          :type="visible ? 'text' : 'password'"
          class="input-block mt-4"
          variant="outlined"
          v-model="password.value.value"
          label="Пароль"
          rounded="lg"
          autocomplete="current-password"
          @click:append-inner="visible = !visible"
        ></v-text-field>
        <p class="sub-title text-start limited-p align-self-start">На почту будет отправлено сообщение для подтверждения</p>
      </form>
      <v-row class="ma-0 pa-0" justify="space-between">
        <v-btn
          @click="emit('change-email', false)"
          class="action-button"
          variant="outlined"
        >Отменить
        </v-btn>
        <v-btn
            @click="submit"
            class="pa-4 submit-button"
            type="submit"
            rounded="lg"
            :disabled="!isFormValid"
            :base-color="isFormValid ? AppColors.BASE_COLOR_100  : AppColors.BASE_COLOR_40"
            :color="isFormValid ? AppColors.ACCENT_COLOR_LIME_100 : AppColors.ACCENT_COLOR_LIME_20"
        >
          Подтвердить
        </v-btn>
      </v-row>
    </v-col>
  </v-row>

</template>

<style scoped>
.change-email-block {
  width: 489px;
  padding: 24px;
  border-radius: 8px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.20));
  background: var(--White-color-100, #FFF);

  @media (max-width: 600px) {
    width: 304px;
    padding: 16px;
  }
}

.title{
  font-size: 32px;
  font-weight: 700;
  line-height: 48px;
  font-style: normal;

  @media (max-width: 600px) {
    font-size: 24px;
    line-height: 32px;
  }
}

.sub-title{
  font-size: 16px;
  font-weight: 300;
  line-height: 24px;
  font-style: normal;

  @media (max-width: 600px) {
    font-size: 14px;
    line-height: 20px;
  }
}


.action-button {
  width: 152px;
  border-radius: 12px;
  border: 1px solid var(--Accent-color-Lime-100, #DF3);
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
  text-transform: none;
  height: 56px;

  @media (max-width: 600px) {
    width: auto;
    font-size: 12px;
    line-height: 16px;
    height: 40px;
    padding: 8px!important;
  }
}

.submit-button {
  width: 152px;
  text-transform: none;
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
  height: 56px;

  @media (max-width: 600px) {
    width: auto;
    font-size: 12px;
    line-height: 16px;
    height: 40px;
    padding: 8px!important;
  }
}
</style>
