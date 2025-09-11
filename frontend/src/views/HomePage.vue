<script setup lang="ts">
import IntroductoryBlock from '@/components/home/introductory/IntroductoryBlock.vue'
import QuestionnaireBlock from '@/components/home/QuestionnaireBlock.vue'
import TopCourseBlock from '@/components/home/topCourse/TopCourseBlock.vue'
import ReviewsBlock from '@/components/home/reviews/ReviewsBlock.vue'
import { onMounted } from 'vue'
import { useHomeStore } from '@/stores/Home'

const homeStore = useHomeStore()

onMounted(async () => {
  await homeStore.initHomeStore()
})
</script>

<template>
  <IntroductoryBlock />
  <QuestionnaireBlock />
  <TopCourseBlock v-if="homeStore.courses.length" :courses="homeStore.courses" />
  <v-divider class="d-none d-sm-block"></v-divider>
  <ReviewsBlock v-if="homeStore.feedbacks?.length" :reviews="homeStore.feedbacks" />
</template>

<style scoped></style>
