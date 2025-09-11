<script setup lang="ts">
import {onMounted} from "vue";
import {useRoute, useRouter} from "vue-router";
import {useUser} from "@/stores/User";

const route = useRoute();
const router = useRouter();
const uid = route.params.uid as string;
const token = route.params.token as string;

const userStore = useUser()

onMounted(() => {
  userStore.setDataResetPasswordEmail(uid, token)
  router.push("/reset-password")
});
</script>

<template>
  <div class="flex items-center justify-center h-screen">
    <p class="text-lg">Сброс и изменение пароля...</p>
  </div>
</template>

<style scoped>

</style>
