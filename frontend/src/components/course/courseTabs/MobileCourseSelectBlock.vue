<script setup lang="ts">
import { ref } from 'vue'
import { useMockCoursesStore } from '@/stores/Mock'
import InternalReviewBlock from '@/components/course/courseTabs/InternalReviewBlock.vue'
import QuestionBlock from '@/components/course/courseTabs/QuestionBlock.vue'
import AuthorCourseCard from '@/components/course/courseTabs/AuthorCourseCard.vue'
import OtherCoursesAuthor from '@/components/course/courseTabs/OtherCoursesAuthor.vue'
import SelectItem from '@/components/course/courseTabs/SelectItem.vue'
import { useCourseStore } from '@/stores/Course'

// Определяем типы для вкладок
interface Tab {
  title: string
  value: string
}

// Реф для управления выбранной вкладкой
const selectedTab = ref<string>('about_course') // По умолчанию "О курсе"

// Данные для вкладок
const mockStore = useMockCoursesStore()
const courseStore = useCourseStore()
const aboutCourseTabContent = mockStore.getContentAboutCourseTab
const paymentTabContent = mockStore.getContentPaymentTab

const tabs: Tab[] = [
  { title: 'О курсе', value: 'about_course' },
  { title: 'Оплата', value: 'payment' },
  { title: 'Отзывы', value: 'reviews' },
  { title: 'Частые Вопросы', value: 'FAQ' },
  { title: 'Автор', value: 'author' },
]
</script>

<template>
  <div class="d-sm-none pa-0 ga-4" style="display: grid; grid-template-columns: 100%">
    <v-select
      class="main-select"
      v-model="selectedTab"
      :items="tabs"
      item-title="title"
      item-value="value"
      variant="outlined"
    />

    <div>
      <SelectItem
        v-if="selectedTab === 'about_course'"
        :server-html="courseStore.course?.description"
      />
      <SelectItem v-if="selectedTab === 'payment'" :server-html="paymentTabContent">
        <div
          v-if="courseStore.course?.return_conditions"
          v-html="courseStore.course?.return_conditions"
        />
      </SelectItem>
      <SelectItem v-if="selectedTab === 'reviews'">
        <InternalReviewBlock />
      </SelectItem>
      <SelectItem v-if="selectedTab === 'FAQ'">
        <QuestionBlock />
      </SelectItem>
      <SelectItem v-if="selectedTab === 'author'">
        <AuthorCourseCard v-if="courseStore.course" :author="courseStore.course.author" />
        <OtherCoursesAuthor />
      </SelectItem>
    </div>
  </div>
</template>

<style scoped>
.main-select {
  width: 100%;
}

::v-deep(.v-input__details) {
  display: none;
}

::v-deep(.v-field) {
  border-radius: 12px;
}
</style>
