<script setup lang="ts">
import {provide, ref} from "vue";
import LoginForm from "@/components/login/LoginForm.vue";
import LoginLayout from "@/layouts/LoginLayout.vue";
import SignInWith from "@/components/login/SignInWith.vue";
import LoginTitle from "@/components/login/LoginTitle.vue";
import ForgotPassword from "@/components/login/ForgotPassword.vue";

const isForgotPassword = ref<boolean>(false)
const isEnterValidEmail = ref<boolean>(false);

const handleForgotPassword = (value: boolean) => {
  isForgotPassword.value = value;
};
const handleEnterValidEmail = (value: boolean) => {
  isEnterValidEmail.value = value;
};
provide('isEnterValidEmail', handleEnterValidEmail);
</script>

<template>
  <LoginLayout :is-login="true">
    <LoginTitle  :isForgotPassword="isForgotPassword" :is-login="true"/>
    <LoginForm @forgot-password="handleForgotPassword"  v-if="!isForgotPassword"  />
    <SignInWith v-if="!isForgotPassword"  />
    <ForgotPassword
      @forgot-password="handleForgotPassword"
      v-if="isForgotPassword"
    />
  </LoginLayout>
</template>

<style scoped>
</style>
