<script setup lang="ts">
import {type PropType, ref} from "vue";
import CourseCard from "@/components/common/CourseCard.vue";
import { Swiper, SwiperSlide } from 'swiper/vue';
// import { FreeMode } from 'swiper/modules';
import {useRouter} from "vue-router";
import type {ICourseItem} from "@/api/courses/models";
import type {SwiperOptions} from "swiper/types";


const props = defineProps({
  courses: { type: Array as PropType<ICourseItem[]>, required: true },
});

const swiperCourseRef = ref(null)
const slide = ref(1)
// const modules = ref([FreeMode])

const router = useRouter();

const breakpoints = {
  320:{ slidesPerView:'auto', spaceBetween: 16 },
  960:{ slidesPerView:2, spaceBetween: 16 },
  1280:{ slidesPerView:3, spaceBetween: 32 }
}
</script>

<template>
  <swiper
    v-model="slide"
    class="course-slider"
    ref="swiperCourseRef"
    :slides-per-view="3"
    :breakpoints="breakpoints as SwiperOptions['breakpoints']"
    :loop="true"
    :space-between="32"
  >
    <swiper-slide v-for="(item) in props.courses" :key="item.id" class="slide-category">
      <CourseCard :in-swiper="true" :course="item" />
    </swiper-slide>
  </swiper>
</template>

<style scoped>
.slide-category {
  width: fit-content;
  @media (max-width: 959px) {
    width: 304px;
  }
  @media (max-width: 600px) {
    width: 224px;
  }
}
.course-slider {
  @media (max-width: 959px) {
    margin-right: -16px;
  }
}
</style>
