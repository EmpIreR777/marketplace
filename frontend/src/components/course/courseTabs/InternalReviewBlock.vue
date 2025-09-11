<script setup lang="ts">
import { useCourseStore } from '@/stores/Course'
import { onMounted, ref } from 'vue'
import FeedbackForm from '@/components/common/FeedbackForm.vue'
import FeedbackCard from '@/components/common/FeedbackCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const courseStore = useCourseStore()

const isFeedbackFormVisible = ref(false)

onMounted(() => {
  courseStore.loadFeedbacks()
})
</script>

<template>
  <div class="d-flex flex-column ga-4">
    <h2 class="heading_h5">Отзывы учеников после прохождения курса</h2>

    <BaseButton
      v-if="!isFeedbackFormVisible && courseStore.course?.is_bought"
      class="flex-fill ma-0"
      label="Оставить отзыв"
      type="outline"
      @click="isFeedbackFormVisible = true"
    />

    <FeedbackForm
      v-if="isFeedbackFormVisible && courseStore.course"
      :course-id="courseStore.course?.id"
      @cancel="isFeedbackFormVisible = false"
    />

    <v-row v-if="courseStore.feedbacks.length">
      <v-col
        cols="12"
        sm="6"
        class="px-0 py-3 px-sm-4 py-sm-4"
        v-for="feedback in courseStore.feedbacks"
        :key="feedback.id"
      >
        <FeedbackCard :feedback="feedback" :is-author="!!courseStore.originCourse?.is_my_course" />
      </v-col>
    </v-row>
  </div>
</template>

<style scoped></style>
