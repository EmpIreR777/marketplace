<script setup lang="ts">
import RatingBlock from '@/components/common/RatingBlock.vue'

defineProps({
  title: String,
  rating: Number,
})
</script>

<template>
  <div class="d-flex align-center justify-space-between flex-wrap flex-sm-nowrap">
    <h2 class="course-header_title">{{ title }}</h2>
    <RatingBlock classes="mt-2 mt-sm-1" :rating="rating" />
  </div>
</template>

<style scoped>
.course-header_title {
  font-size: 40px;
  font-style: normal;
  font-weight: 700;
  line-height: 64px;

  @media (max-width: 960px) {
    font-size: 24px;
    line-height: 32px;
  }
}
</style>
