<script setup lang="ts">
import type {ICourseItem } from "@/api/courses/models";
import YellowButton from "@/components/common/YellowButton.vue";
import SliderCourses from "@/components/sliders/SliderCourses.vue";

const props = defineProps<{
    courses: ICourseItem[]
}>()
</script>

<template>
  <div class="section">
    <div class="d-flex align-center justify-space-between title-block">
      <h3 class="heading_h3">ТОП курсы</h3>
      <YellowButton title="Смотреть все" to="/courses"/>
    </div>
    <SliderCourses :courses="props.courses" />
  </div>
</template>

<style scoped>

</style>
