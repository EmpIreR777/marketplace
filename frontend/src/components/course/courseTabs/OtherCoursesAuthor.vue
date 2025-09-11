<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useCoursesStore } from '@/stores/Courses'
import { useCourseStore } from '@/stores/Course'
import SliderCourses from '@/components/sliders/SliderCourses.vue'
import { useRoute } from 'vue-router'

const coursesStore = useCoursesStore()
const courseStore = useCourseStore()
const route = useRoute()

const courseId = computed(() => String(route.params.id))

onMounted(async () => {
  const coursesParams = {
    offset: 0,
    limit: 12,
    author_id: courseStore.course?.author.id,
  }
  coursesStore.loadCoursesList(coursesParams)
})
</script>

<template>
  <div class="" v-if="coursesStore.getOthetAuthorCourses(courseId).length">
    <h2 class="title">Другие курсы автора</h2>
    <SliderCourses :courses="coursesStore.getOthetAuthorCourses(courseId)" />
  </div>
</template>

<style scoped>
.title {
  font-size: 32px;
  font-style: normal;
  font-weight: 700;
  line-height: 48px;
  margin-bottom: 8px;
}
</style>
