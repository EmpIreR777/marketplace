<script setup lang="ts">
import type { TrainingOptionType } from '@/stores/Mock'
import { useDisplay } from 'vuetify'

const props = defineProps<{
  option: TrainingOptionType,
  isActive?: boolean,
  counter: number
}>()

const { xs } = useDisplay()
</script>

<template>
  <v-card
    class="pa-2 pa-md-4 education-option-card"
    elevation="0"
    :height="xs ? '32px' : '110px'"
    :class="{ 'education-option-card--active': props.isActive }"
  >
    <v-card-title class="education-option-card__title pa-0">{{ props.option.title }}</v-card-title>
    <v-card-subtitle class="education-option-card__subtitle pa-0 d-none d-sm-block"
      >{{ props.counter }} предложений
    </v-card-subtitle>
    <div class="d-flex justify-end education-option-card__action">
      <v-img
        class="education-option-card__icon"
        :src="props.option.icon"
        :size="xs ? '1rem' : '1.5rem'"
        cover
      ></v-img>
    </div>
  </v-card>
</template>

<style scoped lang="scss">
.education-option-card {
  user-select: none;
  box-shadow: none;
  border: 1px solid #36394033;
  border-radius: 16px;
  box-sizing: border-box;
  @media (max-width: 600px) {
    display: flex;
    gap: 8px;
    background-color: var(--Base-color-5);
  }

  &--active {
    background-color: $lime-10;
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

.education-option-card__action {
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
