<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { AppColors } from '@/enums/appColors.ts'
import FilterBar from '@/components/filters/FilterBar.vue'
import FiltersPanel from '@/components/filters/FiltersPanel.vue'
import CoursesFilters from '@/components/courses/CoursesFilters.vue'
import OrgRaw from '@/components/reviews/OrgRaw.vue'
import { useRouter } from 'vue-router'
import { useReviewsStore } from '@/stores/Reviews'
import { useDisplay } from 'vuetify'
import type { Recordable } from '@/types'
import CoursesHeader from '@/components/courses/CoursesHeader.vue'
import { CoursesCategoryEnum } from '@/enums/coursesFiltersEnum'

const router = useRouter()
const reviewsStore = useReviewsStore()
const { width } = useDisplay()
const filterListRef = ref()

const isMobile = computed(() => width.value < 767)

const handleSearchUpdate = async (val: string) => {
  reviewsStore.setSearch(val)
  await reviewsStore.loadCoursesFilters()
}

const handleTopFiltersUpdate = async (val: CoursesCategoryEnum) => {
  reviewsStore.setTopFilters(val)
  await reviewsStore.loadCoursesFilters()
}

const handleSortingUpdate = (val: string | null) => {
  reviewsStore.setOrdering(val)
}

const handleVisibilityUpdate = (val: boolean) => {
  reviewsStore.setFilterVisibility(val)
  if (isMobile.value) {
    if (val) {
      document.body.classList.add('fixed-scroll')
    } else {
      document.body.classList.remove('fixed-scroll')
    }
  }
}

const handleFiltersUpdate = async (val: Recordable) => {
  reviewsStore.setFilters(val)
  await reviewsStore.updateFilters()
}

const handleFiltersReset = async () => {
  reviewsStore.resetFilters()
  await reviewsStore.updateFilters()
  // Clear filter inputs
  if (filterListRef.value) {
    filterListRef.value.checkListRef.forEach((checkList: any) => (checkList.search = ''))
  }
}

function goOrgReviews(id: number) {
  router.push({ name: 'OrganizationReviews', params: { id } })
}

onMounted(() => {
  reviewsStore.loadStore()
})

onUnmounted(() => {
  reviewsStore.clearStore()
})
</script>

<template>
  <div class="reviews-page">
    <CoursesHeader
      title="Отзывы"
      :counters="reviewsStore.topFiltersCount"
      :search-input="reviewsStore.search"
      @update-search="handleSearchUpdate"
      @update-filters="handleTopFiltersUpdate"
    />

    <FilterBar
      ref="listContainer"
      :search="reviewsStore.search"
      :sorting="reviewsStore.ordering"
      :active-filters-count="reviewsStore.getActiveFiltersCount"
      :filter-visibility="reviewsStore.isFiltersVisible"
      @update-search="handleSearchUpdate"
      @update-sorting="handleSortingUpdate"
      @update-filters-visibility="handleVisibilityUpdate"
    />

    <div class="reviews-page__main">
      <v-infinite-scroll
        :key="reviewsStore.renderKey"
        :items="reviewsStore.infinteLoaderData"
        :onLoad="reviewsStore.loadOnScroll"
        class="d-flex flex-column ga-4 w-100 overflow-hidden"
      >
        <OrgRaw
          v-for="(el, ndx) in reviewsStore.infinteLoaderData"
          :key="el.id"
          :organization="el"
          :isCollapsed="reviewsStore.isFiltersVisible"
          class="reviews-page__org-raw"
          :style="{
            borderTop: ndx > 0 ? `1px solid ${AppColors.BASE_COLOR_20}` : 'none',
          }"
          @click="goOrgReviews(el.id)"
        />

        <template #empty></template>
      </v-infinite-scroll>

      <Teleport to="header" :disabled="!isMobile">
        <FiltersPanel
          v-if="reviewsStore.isFiltersVisible"
          :is-mobile="isMobile"
          style="min-width: 300px"
          @update-visibility="handleVisibilityUpdate"
          @reset="handleFiltersReset"
        >
          <CoursesFilters
            v-if="reviewsStore.getFiltersCatalog"
            ref="filterListRef"
            :filter-catalog="reviewsStore.getFiltersCatalog"
            :filters="reviewsStore.filters"
            :filters-update="handleFiltersUpdate"
          />
        </FiltersPanel>
      </Teleport>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.reviews-page {
  display: flex;
  flex-direction: column;
  gap: 16px;

  &__main {
    display: flex;
    justify-content: center;
    gap: 32px;
    width: 100%;

    @include md {
      gap: 16px;
    }

    & .filter-container {
      min-width: calc(33.33% - (32px / 1.5)) !important;
      max-width: calc(33.33% - (32px / 1.5)) !important;

      @include md {
        min-width: calc(50% - (16px / 2)) !important;
        max-width: calc(50% - (16px / 2)) !important;
      }
    }
  }

  &__org-raw {
    padding-bottom: 0;
    cursor: pointer;
  }
}
</style>
