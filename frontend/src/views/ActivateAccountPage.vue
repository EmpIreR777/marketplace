<script setup lang="ts">
import {onMounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {useUser} from "@/stores/User";
import LoadingDialog from "@/components/login/LoadingDialog.vue";
import BaseButton from "@/components/common/BaseButton.vue";

const route = useRoute();
const router = useRouter();

const uid = route.params.uid as string;
const token = route.params.token as string;
const isLoading = ref(false);
const isError = ref(false);
const userStore = useUser()

const registerUser = async () => {
  try {
    isLoading.value = true
    await userStore.finalRegister({ uid, token });
    await router.push("/confirm-register");
  } catch (error) {
    isError.value = true
    console.error("Registration failed:", error);
  } finally {
    isLoading.value = false
  }
};

onMounted(registerUser);
</script>

<template>
  <LoadingDialog v-model="isLoading" />
  <v-card height="100vh" class="d-flex justify-center align-center flex-column">
    <h1 v-if="isError">При активации аккаунта произошла ошибка</h1>
    <BaseButton class="mt-4" to="/" label="На главную" />
  </v-card>
</template>

