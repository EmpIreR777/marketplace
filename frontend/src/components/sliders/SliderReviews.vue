<script setup lang="ts">
import { ref} from "vue";
import { Swiper, SwiperSlide } from 'swiper/vue';
import ReviewCard from "@/components/home/reviews/ReviewCard.vue";
import type {SwiperOptions} from "swiper/types";
import type {IFeedback} from "@/api/feedbacks/models";


const props = defineProps<{
  items: IFeedback[]
}>()

const swiperCourseRef = ref(null)
const slide = ref(1)
const breakpoints = {
  320: { slidesPerView:'auto', spaceBetween: 16 },
  960: { slidesPerView:2, spaceBetween: 16 },
  1280: { slidesPerView:3, spaceBetween: 32 }
}
</script>

<template>
  <swiper
    v-model="slide"
    class="review-slider"
    ref="swiperCourseRef"
    :breakpoints="breakpoints as SwiperOptions['breakpoints']"
    :loop="true"
    :space-between="32"
  >
    <swiper-slide v-for="(item) in props.items" :key="item.id" class="slide-review">
      <ReviewCard :item="item"/>
    </swiper-slide>
  </swiper>
</template>

<style scoped>
.review-slider {
  @media (max-width: 959px) {
    margin-right: -16px;
  }
}
.slide-review {
  width: fit-content;
  @media (max-width: 959px) {
    width: 304px;
  }
  @media (max-width: 600px) {
    width: 224px;
  }
}
</style>
