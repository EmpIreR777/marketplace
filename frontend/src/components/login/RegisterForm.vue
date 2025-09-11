<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useField, useForm } from 'vee-validate'
import * as yup from 'yup'
import { AxiosError } from 'axios'
import LoadingDialog from '@/components/login/LoadingDialog.vue'
import { AppColors } from '@/enums/appColors.ts'
import { useUser } from '@/stores/User'
import type { IUserRegisterBody } from '@/api/user/models'
import { AccountTypeEnum } from '@/enums/userEnum.ts'
import { useMetrika } from '@/composable/useMetrika'
import personalDataConsent from '@/assets/docs/personal_data_consent.pdf'
import userAgreement from '@/assets/docs/user_agreement.pdf'

const { studentRegistration, authorRegistration } = useMetrika()

const userStore = useUser()
const router = useRouter()
const visible = ref(false)
// Обновлённая схема валидации
const { handleSubmit, validate, errors } = useForm({
  validationSchema: yup.object({
    email: yup.string().required().email(),
    password: yup.string().required().min(2),
    confirmPassword: yup
      .string()
      .required('Повторите пароль')
      .oneOf([yup.ref('password')], 'Пароли должны совпадать'),
    role: yup.string().required('Выберите роль'),
    checkPersonalDataConsent: yup
      .boolean()
      .oneOf([true], 'Вы должны согласиться с обработкой данных')
      .required(),
    checkUserAgreement: yup
      .boolean()
      .oneOf([true], 'Вы должны согласиться с правилами пользовательского соглашения')
      .required(),
  }),
})

const email = useField<string>('email')
const password = useField<string>('password')
const confirmPassword = useField<string>('confirmPassword')
const role = useField<string>('role')

const checkPersonalDataConsent = useField('checkPersonalDataConsent')
const checkUserAgreement = useField('checkUserAgreement')

const isFormValid = ref(false)
const isLoading = ref(false)
const isSetError = ref(false)

const checkValidity = async () => {
  await validate()
  return Object.keys(errors.value).length === 0
}

const updateValidity = async () => {
  isFormValid.value = await checkValidity()
}

// Watchers для обновления состояния формы
watch(
  [
    email.value,
    password.value,
    confirmPassword.value,
    role.value,
    checkPersonalDataConsent.value,
    checkUserAgreement.value,
  ],
  () => {
    updateValidity()
  },
)

const submit = handleSubmit(async (values) => {
  isLoading.value = true
  userStore.setTemporaryMail(values.email)

  const body: IUserRegisterBody = {
    email: values.email,
    password: values.password,
    re_password: values.confirmPassword,
    role: values.role,
  }
  // console.log(body)
  try {
    await userStore.createUser(body)

    if (body.role === AccountTypeEnum.STUDENT) {
      studentRegistration()
    }
    if (body.role === AccountTypeEnum.AUTHOR) {
      authorRegistration()
    }

    await router.push('/confirm-register')
  } catch (error) {
    isSetError.value = true
    const errorMessage =
      error instanceof AxiosError ? error.response?.data.errors[0].detail : 'Неизвестная ошибка'
    confirmPassword.setErrors([errorMessage])
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <form @submit.prevent="submit" class="register-form">
    <v-text-field
      class="input-block"
      variant="outlined"
      v-model="email.value.value"
      label="Email"
      rounded="lg"
    ></v-text-field>

    <v-text-field
      class="mt-1 input-block"
      variant="outlined"
      v-model="password.value.value"
      label="Пароль"
      rounded="lg"
      autocomplete="password"
      :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
      :type="visible ? 'text' : 'password'"
      @click:append-inner="visible = !visible"
    ></v-text-field>

    <v-text-field
      class="mt-1 input-block"
      variant="outlined"
      v-model="confirmPassword.value.value"
      label="Повторите пароль"
      rounded="lg"
      :error-messages="isSetError ? confirmPassword.errorMessage.value : ''"
      autocomplete="confirmPassword"
      :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
      :type="visible ? 'text' : 'password'"
      @click:append-inner="visible = !visible"
    ></v-text-field>

    <v-radio-group v-model="role.value.value" column class="mt-1">
      <v-radio label="Я студент" :value="AccountTypeEnum.STUDENT" />
      <v-radio label="Я автор курсов" :value="AccountTypeEnum.AUTHOR" />
    </v-radio-group>

    <v-checkbox v-model="checkPersonalDataConsent.value.value" type="checkbox">
      <template #label>
        <span class="text-body-1">
          Я даю
          <a :href="personalDataConsent" target="_blank" :style="{ color: AppColors.MAIN_TEXT }">
            cогласие на обработку персональных данных
          </a>
        </span>
      </template>
    </v-checkbox>

    <v-checkbox v-model="checkUserAgreement.value.value" type="checkbox">
      <template #label>
        <span class="text-body-1">
          Я ознакомлен и принимаю
          <a :href="userAgreement" target="_blank" :style="{ color: AppColors.MAIN_TEXT }">
            правила пользовательского соглашения
          </a>
        </span>
      </template>
    </v-checkbox>

    <v-btn
      class="mt-6 w-100 pa-4 submit-button"
      type="submit"
      height="56"
      rounded="lg"
      :disabled="!isFormValid"
      :base-color="isFormValid ? AppColors.BASE_COLOR_100 : AppColors.BASE_COLOR_40"
      :color="isFormValid ? AppColors.ACCENT_COLOR_LIME_100 : AppColors.ACCENT_COLOR_LIME_20"
    >
      Зарегистрироваться
    </v-btn>
  </form>

  <LoadingDialog v-model="isLoading" />
</template>
<style scoped lang="scss">
.register-form {
  margin-top: 5px;
}

.submit-button {
  text-transform: none;
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
}

::v-deep(.forgot-password .v-btn__content) {
  border-bottom: 1px solid var(--Base-color-80, rgba(54, 57, 64, 0.8));
}

::v-deep(.v-field--error:not(.v-field--disabled) .v-label.v-field-label) {
  color: var(--Base-color-100, #363940) !important;
}

::v-deep(.v-field--error:not(.v-field--disabled) .v-field__outline) {
  color: var(--Base-color-100, #363940) !important;
}
</style>
