<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router' // Импортируем useRouter
import { useDisplay } from 'vuetify'
import CourseCard from '@/components/common/CourseCard.vue'
import { useCoursesStore } from '@/stores/Courses'
import CoursesFilterMenu from './coursesFilters/CoursesFilterMenu.vue'
import FiltersPanel from '@/components/filters/FiltersPanel.vue'
import { useCoursesFilterStore } from '@/stores/CoursesFilter'
import { FILTER_PROPERTIES_NAMES } from '@/api/coursesFilters/constants'

const props = defineProps<{
  isFilterMenuOpen: boolean
}>()

const emits = defineEmits<{
  (e: 'toggleFilterMenu'): void
}>()

const coursesStore = useCoursesStore()
const coursesFilterStore = useCoursesFilterStore()

// Получаем экземпляр маршрутизатора
const route = useRoute()
const { xs, sm } = useDisplay()
const isMobile = computed(() => xs.value || sm.value)

const resetFilterSelections = async () => {
  coursesFilterStore.clearSelectedCheckboxFilters()
  coursesFilterStore.setSelectedFilters({
    [FILTER_PROPERTIES_NAMES.price_min]: '',
  })
  coursesFilterStore.setSelectedFilters({
    [FILTER_PROPERTIES_NAMES.price_max]: '',
  })

  await coursesFilterStore.loadCoursesFilters()
  coursesStore.clearCourses()
}
</script>

<template>
  <div class="courses-cards" :class="{ filter: props.isFilterMenuOpen }">
    <v-infinite-scroll
      v-if="coursesStore.isScrollActive"
      :items="coursesStore.courses"
      :onLoad="({ done }) => coursesStore.loadMoreCourses(done, route)"
    >
      <div class="courses-cards__grid">
        <template v-for="course in coursesStore.courses">
          <CourseCard class="courses-card" :course="course" />
        </template>
      </div>
      <template v-slot:loading>
        <div class="courses-cards__loader-container">
          <v-progress-circular indeterminate />
        </div>
      </template>
      <template v-slot:empty></template>
    </v-infinite-scroll>

    <Teleport to="header" :disabled="!isMobile">
      <FiltersPanel
        v-if="props.isFilterMenuOpen"
        :is-mobile="isMobile"
        @reset="resetFilterSelections"
        @update-visibility="emits('toggleFilterMenu')"
      >
        <CoursesFilterMenu
          v-if="props.isFilterMenuOpen"
          class="d-none d-sm-flex pa-0"
          :class="['course-filter', { fade: props.isFilterMenuOpen }]"
        />
      </FiltersPanel>
    </Teleport>
  </div>
</template>
<style lang="scss">
.courses-cards {
  display: flex;
  justify-content: center;
  gap: 32px;
  width: 100%;
  flex-wrap: wrap;

  &__loader-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 12px;
  }

  & .v-infinite-scroll {
    overflow: hidden;
    width: 100%;
  }

  &.filter .v-infinite-scroll {
    width: calc(66.66% - (32px / 3));
    @include md {
      width: calc(66.66% - (16px / 3));
    }
    @include sm {
      width: calc(50% - 16px);
    }
  }

  & .v-infinite-scroll__side {
    padding: 0;
  }

  .filter-container {
    width: calc(33.33% - (32px / 1.5));
    @include md {
      width: calc(33.33% - (16px / 1.5));
    }
  }
  @include md {
    gap: 16px;
  }
  .courses-card {
    height: fit-content !important;
    width: calc(33.33% - (32px / 1.5));

    @include md {
      width: calc(33.33% - (16px / 1.5));
    }
    @include sm {
      width: calc(50% - (16px / 2));
    }
    @include xs {
      width: 100%;
    }
  }
  &.filter {
    .courses-card {
      width: calc(50% - (32px / 2));
      @include md {
        width: calc(50% - (16px / 2));
      }
    }
    @include xs {
      grid-template-columns: 1fr;
    }
  }

  &__grid {
    width: 100%;
    gap: 32px;
    display: flex;
    flex-wrap: wrap;

    @include md {
      gap: 16px;
    }
  }
}

.course-filter {
  position: relative;
  transition: $transition;
  overflow: hidden;
  opacity: 0;
  width: 0;
}

.course-filter.fade {
  opacity: 1;
  width: auto;
}
</style>
