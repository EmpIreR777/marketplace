<script setup lang="ts">
import { ref, watch} from "vue";
import {useField, useForm} from "vee-validate";
import * as yup from "yup";
import YellowButton from "@/components/common/YellowButton.vue";
import {AppColors} from "@/enums/appColors.ts";
import {useUser} from "@/stores/User";
import LoginLayout from "@/layouts/LoginLayout.vue";


const userStore = useUser()
const infoTitle = ref<string>('Забыл пароль');

const { handleSubmit, validate, errors } = useForm({
  validationSchema: yup.object({
    password: yup.string().required().min(2),
    passwordRepeat: yup.string().required().min(2).oneOf([yup.ref("password")]),
  }),
});

const password = useField<string>('password')
const passwordRepeat = useField<string>('passwordRepeat')
const visible = ref(false)
const checkValidity = async () => {
  await validate()
  return Object.keys(errors.value).length === 0
}

const updateValidity = async () => {
  isFormValid.value = await checkValidity()
}

// Watchers для обновления состояния формы
watch([ password.value, passwordRepeat.value], () => {
  updateValidity()
})

const transitionNewPassword = ref<boolean>(true)
const enterNewPassword = ref<boolean>(false)
const passwordWasChange = ref<boolean>(false)
const isFormValid = ref(false)

watch(() => userStore.isActivated, (newVal) => {
  if (newVal) {
    transitionNewPassword.value = false;
    enterNewPassword.value = true;
    infoTitle.value = "Изменить пароль"
  }
}, { immediate: true });

const submit = handleSubmit(values => {
  userStore.changeNewPassword({new_password: values.password, uid: userStore.getUid, token: userStore.getResetToken})
  enterNewPassword.value = false
  passwordWasChange.value = true
  infoTitle.value = "Успешно!"
})
</script>

<template>
  <LoginLayout :is-login="true">
    <h5 class="heading_h5 text-center align-center justify-center">{{infoTitle}}</h5>
    <v-row v-if="transitionNewPassword" align="center" justify="center" class="pa-0 title-block">
      <v-col class="ma-0 first-block d-flex flex-column ga-6" cols="auto">
        <p class="lg text-center">Мы отправили письмо для сброса пароля на ваш email
          <span class="lgb">{{userStore.getTemporaryMail? userStore.getTemporaryMail : ''}}</span>
        </p>
        <p class="lg text-center limited-p align-self-center">Перейдите по ссылке в письме для продолжения восстановления доступов</p>
      </v-col>
    </v-row>
    <form v-if="enterNewPassword" @submit.prevent="submit" class="mt-6">
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
        v-model="passwordRepeat.value.value"
        label="Пароль"
        rounded="lg"
        type="password"
        autocomplete="passwordRepeat"
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
        Отправить
      </v-btn>
    </form>
    <v-row v-if="passwordWasChange" align="center" justify="center" class="pa-0 title-block">
      <v-col class="ma-0 first-block d-flex flex-column ga-6" cols="auto">
        <p class="lg text-center">
          Ваш пароль успешно изменён.
        </p>
        <p class="lg text-center">
          Вы можете продолжить своё обучение
        </p>
        <YellowButton custom-class="w-75 mx-auto" title="Перейти на сайт" link="/" />
      </v-col>
    </v-row>
  </LoginLayout>
</template>

<style scoped>
.first-block {
  width: 441px;
}

.limited-p {
  width: 240px;
}

form {
  width: 391px;

  @media (max-width: 600px) {
    width: 336px;
  }
}

.submit-button {
  text-transform: none;
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
}


::v-deep(.forgot-password .v-btn__content){
  border-bottom: 1px solid var(--Base-color-80, rgba(54, 57, 64, 0.80));
}
</style>
