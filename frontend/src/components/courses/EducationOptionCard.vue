<script setup lang="ts">

import type { TrainingOptionType } from "@/stores/Mock";

defineProps({
  option: {
    type: Object as () => TrainingOptionType,
    required: true,
  },
});
</script>

<template>
  <v-card class="pa-2 pa-md-4 education-option-card">
    <v-card-title class="education-option-card__title pa-0">{{ option.title }}</v-card-title>
    <v-card-subtitle class="education-option-card__subtitle pa-0 d-none  d-sm-block">{{ option.subtitle }} предложений
    </v-card-subtitle>
    <div class="d-flex justify-end education-option-card__action">
      <v-img
        class="education-option-card__icon"
        :src="option.icon"
        width="24"
        height="24"
        cover
      ></v-img>
    </div>
  </v-card>
</template>

<style scoped>
.education-option-card {
  width: 176px;
  height: 110px;
  user-select: none;

  @media (max-width: 600px) {
    display: flex;
    gap: 8px;
    height: 32px;
    width: auto;
  }
}

.education-option-card__title {
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;

  @media (max-width: 600px) {
    font-size: 12px;
    font-style: normal;
    font-weight: 700;
    line-height: 16px; /* 133.333% */
  }
}

.education-option-card__subtitle {
  font-size: 12px;
  font-style: normal;
  font-weight: 300;
  line-height: 16px;
}

.education-option-card__action{
  margin-top: 14px;

  @media (max-width: 600px) {
    margin-top: 0;
    order: -1;
  }
}

.education-option-card__icon {
  flex-grow: 0;
  width: 24px;
  height: 24px;

  @media (max-width: 600px) {
    width: 16px;
    height: 16px;
  }
}
</style>
