<script setup lang="ts">
import { ref, type PropType } from "vue";
import { Swiper, SwiperSlide } from 'swiper/vue';
import type { Swiper as SwiperInstance } from 'swiper'
import type { IQuizQuestion } from '@/api/quiz/models'
import QuestionSlide from "./QuestionSlide.vue";
import FinalSlide from "./FinalSlide.vue";
import { useQuestionnaireStore } from '@/stores/Questionnaire';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps({
  questionnaireData: {
    type: Array as PropType<IQuizQuestion[]>,
    required: true,
  },
  isVisible: {
    type: Boolean,
  },
});

const questionnaireStore = useQuestionnaireStore()

const swiperRef = ref<SwiperInstance | null>(null);

const onSwiper = (swiper: SwiperInstance) => {
  swiperRef.value = swiper;
};

const prev = () => {
  if (!swiperRef.value) {
    return
  }
  swiperRef.value.slidePrev();  // Метод для движения назад
};

const next = () => {
  if (!swiperRef.value) {
    return
  }
  swiperRef.value.slideNext();  // Метод для движения вперед
};
</script>


<template>
  <swiper
    :v-model="questionnaireData"
    class="questionnaire-swiper"
    :class="{ visible: isVisible }"
    ref="swiperRef"
    :allow-touch-move="false"
    :slides-per-view="1"
    :space-between="50"
    @swiper="onSwiper"
  >
    <swiper-slide  v-for="(item) in questionnaireData" :key="item.id">
      <QuestionSlide v-if="!questionnaireStore.getIsLastQuestion" :data="item" @prev="prev" @next="next" />
      <FinalSlide v-else/>
    </swiper-slide>
  </swiper>
</template>

<style scoped>
.questionnaire-swiper{
  transform: translateX(110%);
  transition: transform .3s ease-in-out;
}
.questionnaire-swiper.visible{
  transform: translateX(0);
}
</style>

