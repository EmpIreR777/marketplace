<script setup lang="ts">
import { ref } from 'vue'
import { useMockCoursesStore } from '@/stores/Mock'
import TabItem from '@/components/course/courseTabs/TabItem.vue'
import InternalReviewBlock from '@/components/course/courseTabs/InternalReviewBlock.vue'
import type { ICourseDetail } from '@/api/courses/models'
import QuestionBlock from '@/components/course/courseTabs/QuestionBlock.vue'
import AuthorCourseCard from '@/components/course/courseTabs/AuthorCourseCard.vue'
import OtherCoursesAuthor from '@/components/course/courseTabs/OtherCoursesAuthor.vue'
import { useCourseStore } from '@/stores/Course'

defineProps<{
  courseData: ICourseDetail
}>()

const mockStore = useMockCoursesStore()
const courseStore = useCourseStore()
const tabs = mockStore.getTabsCoursePage
const paymentTabContent = mockStore.getContentPaymentTab
const tab = ref(null)
</script>

<template>
  <v-card class="pa-0 d-none d-sm-block" elevation="0">
    <v-tabs
      v-model="tab"
      bg-color="transparent"
      class="px-1 py-2 course-tabs-container"
      height="72"
      grow
    >
      <v-tab
        class="lg text-capitalize rounded-lg mx-1"
        v-for="tab in tabs"
        :key="tab.id"
        :value="tab.value"
        height="56"
        selected-class="active-course-tab"
      >
        {{
          tab.value === 'reviews'
            ? `${tab.name} (${courseStore.course?.feedbacks_count || 0})`
            : tab.name
        }}
      </v-tab>
    </v-tabs>

    <v-card-text>
      <v-tabs-window v-model="tab">
        <TabItem
          v-if="courseData.description"
          tab-value="about_course"
          :server-html="courseData.description"
        />
        <TabItem tab-value="payment" :server-html="paymentTabContent">
          <div
            v-if="courseStore.course?.return_conditions"
            v-html="courseStore.course?.return_conditions"
          />
        </TabItem>
        <TabItem tab-value="reviews">
          <InternalReviewBlock />
        </TabItem>
        <TabItem tab-value="FAQ">
          <QuestionBlock />
        </TabItem>
        <TabItem tab-value="author">
          <AuthorCourseCard v-if="courseStore.course" :author="courseStore.course.author" />
          <OtherCoursesAuthor />
        </TabItem>
      </v-tabs-window>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.course-tabs-container {
  border-radius: 12px;
  border: 1px solid var(--Base-color-10, rgba(54, 57, 64, 0.1));
}

.active-course-tab {
  border-radius: 8px;
  background: var(--Accent-color-Lime-100, #df3);
  font-weight: 700;
}
</style>
