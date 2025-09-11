<script setup lang="ts">
import { useMockCoursesStore } from '@/stores/Mock'

const mockStore = useMockCoursesStore()
const questionItems = mockStore.getContentCourseQuestions
</script>

<template>
  <div class="ma-0">
    <h2 class="heading_h5">Частые Вопросы</h2>
    <v-row class="ma-0 pa-0 mt-5">
      <div v-for="item in questionItems" :key="item.id" class="w-100 my-3">
        <div class="faq-question">{{ item.question }}</div>
        <div class="faq-answer mt-2">{{ item.answer }}</div>
      </div>
    </v-row>
  </div>
</template>

<style scoped>
.faq-question {
  font-size: 24px;
  font-style: normal;
  font-weight: 700;
  line-height: 32px;
}

.faq-answer {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
}
</style>
