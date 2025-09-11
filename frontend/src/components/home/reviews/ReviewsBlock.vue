<script setup lang="ts">
import SliderReviews from "@/components/sliders/SliderReviews.vue";
import YellowButton from "@/components/common/YellowButton.vue";
import type {IFeedback} from "@/api/feedbacks/models";

const props = defineProps<{
  reviews: IFeedback[]
}>()
</script>

<template>
  <div class="section">
    <div class="d-flex align-center justify-space-between title-block">
      <h3 class="heading_h3 title">Отзывы</h3>
      <YellowButton title="Смотреть все" to="/reviews"/>
    </div>
    <SliderReviews :items="props.reviews" />
  </div>
</template>

<style scoped>

</style>
