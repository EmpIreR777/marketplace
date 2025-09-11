<script setup lang="ts">
import {ref, watch} from "vue";
import {useRouter} from "vue-router";
import * as yup from 'yup'
import {useField, useForm} from 'vee-validate'
import {useUser} from "@/stores/User";
import {AppColors} from "@/enums/appColors.ts";

interface Cause {
  title: string;
  value: string;
}

const options: Cause[] = [
  {title: 'Причина1', value: 'cause1'},
  {title: 'Причина2', value: 'cause2'},
  {title: 'Причина3', value: 'cause3'},

];

const userStore = useUser()
const router = useRouter()
const visible = ref(false)
const { handleSubmit, validate, errors } = useForm({
  validationSchema: yup.object({
    password: yup.string().required().min(2),
    checkbox: yup.boolean().oneOf([true], 'Вы должны согласиться с обработкой данных').required(),
    selectedTab: yup.string().notOneOf([''], 'Выберите причину удаления').required(),
  }),
});
const selectedTab = useField<string>('selectedTab', undefined, { initialValue: 'cause1' });
const password = useField<string>('password')
const checkbox = useField('checkbox')

const isFormValid = ref(false)
const isLoading = ref(false)
const isSetError = ref(false);

const checkValidity = async () => {
  await validate()
  return Object.keys(errors.value).length === 0
}

const updateValidity = async () => {
  isFormValid.value = await checkValidity()
}

watch([ password.value, checkbox.value], () => {
  updateValidity()
})

const submit = handleSubmit(async (values) => {
  isLoading.value = true;

  const body: {password: string} = {
    password: values.password,
  };
  try {
    await userStore.deleteUserForViewing(body)
    userStore.logoutUser(router)
  } catch (error) {
    isSetError.value = true
    const errorMessage = error instanceof Error ? error.message : "Неизвестная ошибка";
    password.setErrors([errorMessage]);
  } finally {
    isLoading.value = false;
  }
});
</script>
<template>
  <v-container class="pa-0 ma-0 content">
    <h2 class="heading_h6 mt-3">Удалить учетную запись</h2>
    <h4 class="lgb mt-5">Хотите удалить свою учетную запись?</h4>
    <p class="lg mt-4">
      Эта учётной записи приведёт к удалению информации о всех купленных или опубликованных вами курсах.
    </p>
    <p class="lg mt-2">
      Удаление будет <span class="lgb">НЕОБРАТИМЫМ</span>, без возможности восстановления. Вы сразу же потеряете доступ к своей учётной записи.
    </p>
    <form @submit.prevent="submit" class="mt-4">
      <v-checkbox
        v-model="checkbox.value.value"
        label="Я даю согласие на обработку моих персональных данных"
        type="checkbox"
        value="1"
      ></v-checkbox>
      <v-select
        class="width-block mt-6"
        v-model="selectedTab.value.value"
        :items="options"
        item-title="title"
        item-value="value"
        variant="outlined"
        rounded="lg"
      ></v-select>
      <v-text-field
        class="mt-4 width-block"
        variant="outlined"
        v-model="password.value.value"
        label="Пароль"
        rounded="lg"
        autocomplete="password"
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        @click:append-inner="visible = !visible"
      ></v-text-field>
      <v-btn
        class="mt-6 pa-4 submit-button width-block"
        type="submit"
        rounded="lg"
        :disabled="!isFormValid"
        :base-color="isFormValid ? AppColors.BASE_COLOR_100  : AppColors.BASE_COLOR_40"
        :color="isFormValid ? AppColors.ACCENT_COLOR_LIME_100 : AppColors.ACCENT_COLOR_LIME_20"
      >
        Удалить учётную запись
      </v-btn>
    </form>
  </v-container>
</template>

<style scoped>
.content{
  width: 615px;

  @media (max-width: 960px) {
    width: 100%;
  }
}

.width-block{
  width: 280px;
}

.submit-button {
  text-transform: none;
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
  height: 56px;
}
</style>
