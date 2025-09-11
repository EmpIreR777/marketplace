<script setup lang="ts">
defineProps({
  title: String,
  value: Number,
})
</script>

<template>
  <v-card elevation="0" class="number-card" outlined>
    <div class="card-content">
      <h5 class="card-content-number">{{ value }}</h5>
      <p class="card-content-title">{{ title }}</p>
    </div>
  </v-card>
</template>

<style scoped lang="scss">
.number-card {
  background-color: var(--Accent-color-Lime-100);
  color: var(--Base-color-100);
  width: calc(25% - 8px);
  text-align: center;
  padding: 32px;
  border-radius: 16px;
  height: auto;
  min-height: 0;
  @media (max-width: 1279px) {
    padding: 16px 8px;
  }
  @media (max-width: 960px) {
    width: calc(50% - 8px);
    padding: 16px 8px;
  }
  @include xs {
    border-radius: 8px;
  }
}

.card-content-number {
  font-size: 32px;
  font-weight: 700;
  line-height: 48px;

  @media (max-width: 960px) {
    font-size: 12px;
    font-weight: 300;
    line-height: 16px;
  }
}

.card-content-title {
  font-size: 16px;
  font-weight: 300;
  line-height: 24px;

  @media (max-width: 960px) {
    font-size: 14px;
    font-weight: 700;
    line-height: 20px;
  }
}
</style>
