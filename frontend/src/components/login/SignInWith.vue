<script setup lang="ts">
import {
  appleIcon,
  yandexIcon,
  vkontakteIcon,
  classmatesIcon,
  googleIcon,
} from '@/assets/login/sign-in-with'

const signInOptions = [yandexIcon, classmatesIcon, vkontakteIcon, googleIcon, appleIcon]
</script>

<template>
  <v-row class="mt-16 mx-0 mb-0 flex-column ga-6" justify="center" align="center">
    <h6 class="heading_h6">Войти с помощью</h6>
    <v-col cols="auto" class="d-flex ga-4 pa-0">
      <v-btn
        class="sign-in-option"
        variant="text"
        v-for="(option, index) in signInOptions"
        :key="index"
        disabled
      >
        <v-img width="24" height="24" cover :src="option"></v-img>
      </v-btn>
    </v-col>
  </v-row>
</template>

<style scoped>
.sign-in-option {
  border-radius: 8px;
  background: var(--Accent-color-Lime-100, #df3);
  width: 32px;
  height: 32px;
  flex-grow: 0;
  min-width: unset;
}
</style>
