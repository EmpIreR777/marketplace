<script setup lang="ts">
import type { ICourseItem } from '@/api/courses/models'
import { AppColors } from '@/enums/appColors.ts'
import { formatTime } from '@/utils/helpers.ts'
import { imageOutline } from '@/assets/icons'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'

defineProps<{
  course: ICourseItem
  inSwiper?: boolean
  isEditable?: boolean
}>()

const router = useRouter()

const goEditCourse = (id: string) => {
  // const url = router.resolve({ name: 'CourseEditor', params: { id } }).href
  // window.open(url, '_blank')
  router.push({ name: 'CourseEditor', params: { id } })
}
</script>

<template>
  <v-card
    elevation="0"
    class="course-card pa-2 pa-sm-4 h-100"
    :class="{ 'width-in-swiper': inSwiper, disabled: course?.is_active === false }"
    :to="{ name: 'CourseDetail', params: { id: course.id } }"
    @click.stop
  >
    <v-img
      class="course-card-img"
      :src="course.course_image ?? imageOutline"
      width="100%"
      min-height="160"
      cover
      draggable="false"
    ></v-img>
    <v-card-text class="position-relative mt-5 py-0 px-2 pa-sm-4">
      <div class="d-flex justify-start align-center ga-1 chip-block">
        <v-chip
          v-if="course.course_duration"
          :color="AppColors.BASE_COLOR_100"
          class="card-chip"
          outlined
        >
          {{ formatTime(course.course_duration).hour }} часов
          {{
            formatTime(course.course_duration).min
              ? `${formatTime(course.course_duration).min} минут`
              : ''
          }}
        </v-chip>
        <v-chip v-if="course.startDate" color="AppColors.BASE_COLOR_100" class="card-chip" outlined>
          {{ course.startDate }}
        </v-chip>
      </div>
      <p class="course-card__title text-truncate">{{ course.name }}</p>
      <h6 v-if="course.price" class="heading_h6 course-card-price mt-sm-2">
        {{ parseFloat(course.price).toLocaleString('ru-RU') }} ₽
      </h6>
    </v-card-text>
    <v-card-actions v-if="isEditable" class="pa-0" style="min-height: initial">
      <BaseButton
        class="course-edit-trigger"
        icon="edit"
        type="icon"
        @click.stop.prevent="goEditCourse(course.id)"
      />
    </v-card-actions>
  </v-card>
</template>

<style lang="scss">
.course-card {
  user-select: none;
  border-radius: 16px;
  border: 1px solid $base-10;

  &__title {
    @include typography('lg');

    @include sm {
      @include typography('md');
    }
  }

  &.disabled {
    opacity: 0.5;
    filter: grayscale(1);
  }
}
.course-card-img {
  // height: 216px;
  border-radius: 8px;
  aspect-ratio: 16 / 9;

  & > .v-img__img {
    @include sm {
      // height: 125px;
      // aspect-ratio: 288 / 165;
    }
  }
}

.chip-block {
  position: absolute;
  left: 16px;
  top: -30px;
  z-index: 100;

  @include md {
    left: 0;
  }
}

.card-chip {
  background-color: #d7eced;

  &.v-chip--size-default {
    padding: 0 8px;
    height: 24px;
  }

  & > .v-chip__content {
    @include typography('sm');
  }
}

.course-card-price {
  @include typography('h6');

  @include sm {
    @include typography('lgb');
  }
}

.course-edit-trigger {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}
</style>
