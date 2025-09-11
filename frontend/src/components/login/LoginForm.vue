<script setup lang="ts">
import {ref, watch} from 'vue'
import {useRouter} from "vue-router";
import {useField, useForm} from 'vee-validate'
import * as yup from 'yup'
import { AxiosError } from 'axios';
import LoadingDialog from "@/components/login/LoadingDialog.vue";
import {AppColors} from "@/enums/appColors.ts"
import {useUser} from "@/stores/User";

// Типизация emit-события
const emit = defineEmits<{
  (event: 'forgot-password', value: boolean): void;
}>();

const router = useRouter();
const userStore = useUser()
const visible = ref(false)
const {handleSubmit, validate, errors} = useForm({
  validationSchema: yup.object({
    email: yup.string().required().email(),
    password: yup.string().required().min(2),
  }),
})

const email = useField<string>('email')
const password = useField<string>('password')

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

// Watchers для обновления состояния формы
watch([email.value, password.value], () => {
  updateValidity()
})

const submit = handleSubmit(async (values) => {
  isLoading.value = true;
  try{
    await userStore.loginUser({email: values.email, password: values.password}, router)
    // router.push('/');
  } catch (error) {
    isLoading.value = false;
    isSetError.value = true;
    const errorMessage = error instanceof AxiosError ? error.response?.data.errors[0].detail : "Неизвестная ошибка";
    password.setErrors([errorMessage]);
  } finally {
    isLoading.value = false;
  }
})
</script>

<template>
  <form @submit.prevent="submit" class="login-form">
    <v-text-field
      class="input-block"
      variant="outlined"
      v-model="email.value.value"
      label="Email"
      rounded="lg"
    ></v-text-field>

    <v-text-field
      :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
      :type="visible ? 'text' : 'password'"
      class="mt-1 input-block"
      variant="outlined"
      v-model="password.value.value"
      label="Пароль"
      rounded="lg"
      :error-messages="isSetError? password.errorMessage.value:''"
      autocomplete="password"
      @click:append-inner="visible = !visible"
    ></v-text-field>

    <v-btn
      class="mt-6 w-100 pa-4 submit-button"
      type="submit"
      height="56"
      rounded="lg"
      :disabled="!isFormValid"
      :base-color="isFormValid ? AppColors.BASE_COLOR_100  : AppColors.BASE_COLOR_40"
      :color="isFormValid ? AppColors.ACCENT_COLOR_LIME_100 : AppColors.ACCENT_COLOR_LIME_20"
    >
      Войти
    </v-btn>
  </form>
  <v-row justify="center" class="mt-6 mx-0" mb-0>
    <v-btn
      variant="text"
      class="forgot-password"
      @click="emit('forgot-password', true)"
    >
      Забыл пароль
    </v-btn>
  </v-row>

  <LoadingDialog v-model="isLoading" />
</template>
<style scoped lang="scss">
.login-form {
  margin-top: 5px;
}

.submit-button {
  text-transform: none;
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
}

.forgot-password {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
  text-transform: none;
}

::v-deep(.forgot-password .v-btn__content){
  border-bottom: 1px solid var(--Base-color-80, rgba(54, 57, 64, 0.80));
}


::v-deep(.v-field--error:not(.v-field--disabled) .v-label.v-field-label){
  color: var(--Base-color-100, #363940)!important;

}

::v-deep(.v-field--error:not(.v-field--disabled) .v-field__outline){
  color: var(--Base-color-100, #363940)!important;
}

</style>
