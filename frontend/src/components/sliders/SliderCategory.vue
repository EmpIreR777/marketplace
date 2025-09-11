<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useMockCoursesStore } from '@/stores/Mock'
import EducationOptionCardNew from '@/components/courses/EducationOptionCardNew.vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { FreeMode } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/free-mode'
import { CoursesCategoryEnum } from '@/enums/coursesFiltersEnum'

const coursesStoreMock = useMockCoursesStore()
const swiperCategoryRef = ref(null)
const slide = ref(1)
const trainingOptions = coursesStoreMock.getAllTrainingOptions
const modules = ref([FreeMode])

const route = useRoute()

const props = defineProps<{
  counters: Record<CoursesCategoryEnum, number>
}>()

const emits = defineEmits<{
  (e: 'update-filters', val: CoursesCategoryEnum): void
}>()

const isActive = computed(() => (item: CoursesCategoryEnum) => route.query.top?.includes(item))
const isDisabled = (key: CoursesCategoryEnum) => !(props.counters?.[key] > 0)
</script>

<template>
  <swiper
    v-model="slide"
    class="category-slider"
    ref="swiperCategoryRef"
    :slides-per-view="'auto'"
    :modules="modules"
    :space-between="8"
  >
    <swiper-slide
      v-for="item in trainingOptions"
      :key="item.id"
      class="slide-category"
      :class="{ disabled: isDisabled(item.key) }"
      @click="!isDisabled(item.key) && emits('update-filters', item.key)"
    >
      <EducationOptionCardNew
        :option="item"
        :is-active="isActive(item.key)"
        :counter="props.counters[item.key]"
      />
    </swiper-slide>
  </swiper>
</template>

<style scoped lang="scss">
.slide-category {
  width: fit-content;
  cursor: pointer;

  &.disabled {
    opacity: 0.4;
  }
}
</style>
