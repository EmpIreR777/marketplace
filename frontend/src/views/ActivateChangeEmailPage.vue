<script setup lang="ts">
import { onMounted } from "vue";
import {useRoute, useRouter} from "vue-router";
import {useUser} from "@/stores/User";

const route = useRoute();
const router = useRouter();
const savedEmail = localStorage.getItem("new_email");
const uid = route.params.uid as string;
const token = route.params.token as string;

const userStore = useUser()

onMounted(() => {
  if(savedEmail)
  userStore.changeUserEmail({uid, token, new_email: savedEmail})
  router.push("/account")
});
</script>

<template>
  <div class="flex items-center justify-center h-screen">
    <p class="text-lg">Активация смены почты</p>
  </div>
</template>

