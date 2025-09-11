<script setup lang="ts">
import { onMounted } from "vue";
import {useRoute, useRouter} from "vue-router";
import {useUser} from "@/stores/User";

const route = useRoute();
const router = useRouter();
const savedPassword = localStorage.getItem("new_password");
const uid = route.params.uid as string;
const token = route.params.token as string;

const userStore = useUser()

onMounted(() => {
  if(savedPassword)
  userStore.resetPasswordConfirm({uid, token, new_password: savedPassword})
  localStorage.removeItem("new_password");
  router.push("/account")
});
</script>

<template>
  <div class="flex items-center justify-center h-screen">
    <p class="text-lg">Активация смены пароля</p>
  </div>
</template>

