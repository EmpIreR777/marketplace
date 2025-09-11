<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useField, useForm } from 'vee-validate'
import * as yup from 'yup'
import LoadingDialog from '@/components/login/LoadingDialog.vue'
import { AppColors } from '@/enums/appColors.ts'
import { useUser } from '@/stores/User'

// Типизация emit-события
const emit = defineEmits<{
  (event: 'forgot-password', value: boolean): void
}>()
const router = useRouter()
const userStore = useUser()

const infoTitle = ref<string>('Забыл пароль')

const { handleSubmit, validate, errors } = useForm({
  validationSchema: yup.object({
    email: yup.string().required().email(),
  }),
})

const email = useField<string>('email')

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
watch([email.value], () => {
  updateValidity()
})

const submit = handleSubmit(async (values) => {
  isLoading.value = true
  userStore.setTemporaryMail(values.email)
  try {
    await userStore.resetPassword({ email: values.email })
    await router.push('/reset-password')
  } catch (error) {
    isLoading.value = false
    console.error('Ошибка при сбросе пароля:', error)

    isSetError.value = true
    email.setErrors([
      'Такой email не зарегестрирован. Проверьте правильность заполнения, либо введите другой адрес',
    ])
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="forgot-password">
    <h5 class="forgot-password__title">{{ infoTitle }}</h5>
    <form @submit.prevent="submit" class="forgot-password__form mt-6">
      <v-text-field
        class="input-block"
        variant="outlined"
        v-model="email.value.value"
        label="Email"
        rounded="lg"
        :error-messages="isSetError ? email.errorMessage.value : []"
        autocomplete="passwordRepeat"
      ></v-text-field>
      <v-btn
        class="mt-6 w-100 pa-4 submit-button"
        type="submit"
        height="56"
        rounded="lg"
        :disabled="!isFormValid"
        :base-color="isFormValid ? AppColors.BASE_COLOR_100 : AppColors.BASE_COLOR_40"
        :color="isFormValid ? AppColors.ACCENT_COLOR_LIME_100 : AppColors.ACCENT_COLOR_LIME_20"
      >
        Отправить
      </v-btn>
    </form>
    <v-row justify="center" class="mt-6 mx-0" mb-0>
      <v-btn variant="text" class="forgot-password" @click="emit('forgot-password', false)">
        Я вспомнил пароль!
      </v-btn>
    </v-row>
    <LoadingDialog v-model="isLoading" />
  </div>
</template>
<style scoped lang="scss">
.forgot-password {
  &__title {
    @include typography('h5');
    color: $base-80;
    text-align: center;
  }
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

::v-deep(.v-field--error:not(.v-field--disabled) .v-label.v-field-label) {
  color: var(--Base-color-100, #363940) !important;
}

::v-deep(.v-field--error:not(.v-field--disabled) .v-field__outline) {
  color: var(--Base-color-100, #363940) !important;
}
</style>
