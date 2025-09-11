<script setup lang="ts">
import { onUnmounted, ref } from 'vue'
import { AppColors } from '@/enums/appColors.ts'
import { useMyCoursesFeedbacksStore } from '@/stores/Account/my-courses-feedbacks'
import FeedbackCard from '@/components/common/FeedbackCard.vue'

const myCoursesFeedbacksStore = useMyCoursesFeedbacksStore()

interface Tab {
  title: string
  value: string
}

const tabs: Tab[] = [
  { title: 'UI/UX Дизайнер (Pro)', value: '1' },
  { title: 'second', value: '2' },
  { title: 'third', value: '3' },
]

const selectedTab = ref<string>('Мои курсы')

onUnmounted(() => {
  myCoursesFeedbacksStore.clearStore()
})
</script>

<template>
  <v-card
    elevation="0"
    :loading="myCoursesFeedbacksStore.isLoading"
    style="display: grid; grid-template-columns: 100%"
  >
    <v-card-title
      class="d-flex align-start flex-wrap flex-md-nowrap justify-space-between pa-0 ga-4"
      style="white-space: wrap"
    >
      <div class="text-h5 font-weight-bold flex-fill" :style="{ color: AppColors.MAIN_TEXT }">
        Отзывы о ваших курсах
      </div>

      <div class="d-flex w-100 w-sm-auto ga-4 ml-auto">
        <v-select
          v-if="false"
          class="w-100 w-sm-auto"
          :min-width="230"
          v-model="selectedTab"
          :items="tabs"
          item-title="title"
          item-value="value"
          variant="outlined"
          rounded="lg"
          hide-details
        />
      </div>
    </v-card-title>

    <v-card-text class="pa-0">
      <v-infinite-scroll
        :items="myCoursesFeedbacksStore.infinteLoaderData"
        :onLoad="myCoursesFeedbacksStore.loadOnScroll"
        class="d-flex justify-center ga-1 w-100"
      >
        <div
          class="w-100 ga-4 ga-md-8"
          style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))"
        >
          <div v-for="el in myCoursesFeedbacksStore.infinteLoaderData" :key="el.id">
            <FeedbackCard :feedback="el" :isAuthor="true" />
          </div>
        </div>

        <template #empty></template>
      </v-infinite-scroll>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss"></style>
