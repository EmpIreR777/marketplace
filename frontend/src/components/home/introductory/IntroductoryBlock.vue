<script setup lang="ts">
import { computed } from 'vue'
import IntroductoryCard from './IntroductoryCard.vue'
import { useHomeStore } from '@/stores/Home'
const homeStore = useHomeStore()

const statisticCourses = computed(() => {
  return homeStore.statistic?.courses ? Math.floor(homeStore.statistic.courses / 1000) * 1000 : 0
})
</script>

<template>
  <div class="introduce-section d-flex flex-column justify-space-between mx-n2 mx-sm-0">
    <div class="introduce-photo-block"></div>
    <v-row justify="start" class="text-left introduce-section-title">
      <!-- Заголовок -->
      <v-col cols="12 pa-0">
        <div class="header-text">
          <h1 class="heading_h3">
            Наша библиотека <br class="d-md-none" />
            насчитывает
          </h1>
          <h2 class="highlight heading_h3">
            более <br class="d-md-none" />
            {{ statisticCourses }} курсов
          </h2>
        </div>
      </v-col>
    </v-row>

    <v-row justify="center" class="number-cards">
      <IntroductoryCard
        v-for="stat in homeStore.getStatistic"
        :key="stat.key"
        :title="stat.key"
        :value="stat.value"
      />
    </v-row>
  </div>
</template>

<style scoped>
.introduce-section {
  position: relative;
  height: 688px;
  color: var(--White-color-100);
  padding: 72px 48px 32px;
  @media (max-width: 600px) {
    height: auto;
    padding: 8px 20px 24px;
  }
}

.introduce-photo-block {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background:
    linear-gradient(0deg, var(--Base-color-100, #363940) 0%, var(--Base-color-100, #363940) 100%),
    linear-gradient(
      270deg,
      rgba(0, 0, 0, 0) 0%,
      rgba(0, 0, 0, 0.56) 48.9%,
      rgba(0, 0, 0, 0.8) 100%
    ),
    url('@/assets/home/introduce.png') lightgray 50% / cover no-repeat;
  background-blend-mode: color, normal, normal;
  border-radius: 32px;
  @media (max-width: 600px) {
    height: 156px;
    border-radius: 16px;
  }
}

.introduce-section-title {
  padding: 64px 80px;
  flex: 0 0 auto;
  z-index: 1;
  @media (max-width: 1279px) {
    padding: 0;
  }
  @media (max-width: 600px) {
    padding: 0;
    margin: 0;
    height: 148px;
  }
}

.header-text {
  width: 638px;

  @media (max-width: 600px) {
    width: 100%;
  }
}

.header-text .highlight {
  color: var(--Accent-color-Lime-100);
}

.number-cards {
  margin: 0;
  flex: 0 0 auto;
  flex-wrap: nowrap;
  gap: 32px;
  @media (max-width: 1279px) {
    padding: 0;
  }
  @media (max-width: 960px) {
    flex-wrap: wrap;
    gap: 16px;
    margin-top: 16px;
  }
}
</style>
