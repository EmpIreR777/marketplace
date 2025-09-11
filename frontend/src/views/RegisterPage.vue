<script setup lang="ts">
import LoginLayout from "@/layouts/LoginLayout.vue";
import RegisterForm from "@/components/login/RegisterForm.vue";
import LoginTitle from "@/components/login/LoginTitle.vue";

</script>

<template>
  <LoginLayout :is-login="false" >
    <LoginTitle  :is-login="false" />
    <RegisterForm />
  </LoginLayout>
</template>
