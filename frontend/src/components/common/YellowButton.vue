<script setup lang="ts">
import { AppColors } from '@/enums/appColors.ts'
defineProps({
  title: String,
  customClass: {
    // Добавляем возможность передавать классы
    type: String,
    default: '',
  },
  link: {
    type: String,
    required: false,
  },
})
</script>

<template>
  <v-btn :to="link" :class="customClass" class="see-all" :color="AppColors.ACCENT_COLOR_LIME_100">{{
    title
  }}</v-btn>
</template>

<style scoped>
.see-all {
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
  height: auto;
  box-shadow: none;
  text-transform: none;

  @media (max-width: 600px) {
    padding: 8px 16px;
    font-size: 12px;
    line-height: 16px;
    border-radius: 8px;
  }
}
</style>
