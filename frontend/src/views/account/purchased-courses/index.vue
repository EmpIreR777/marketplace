<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useDisplay } from 'vuetify'
import CourseCard from '@/components/common/CourseCard.vue'
import SortingBar from '@/components/filters/SortingBar.vue'
import FilterTrigger from '@/components/filters/FilterTrigger.vue'
import FiltersPanel from '@/components/filters/FiltersPanel.vue'
import { usePurchasedCoursesStore } from '@/stores/Account/purchased-courses'
import { API_ORDERING_KEYS, SORTING_FIELDS_TRANSLATE } from '@/enums/coursesFiltersEnum'
import type { Recordable } from '@/types'
import BaseTextField from '@/components/common/BaseTextField.vue'
import CoursesFilters from '@/components/courses/CoursesFilters.vue'

const purchasedCoursesStore = usePurchasedCoursesStore()
const { xs, sm } = useDisplay()
const isMobile = computed(() => xs.value || sm.value)
const filterListRef = ref()

const sortingItems = computed(() => [
  {
    apiKey: API_ORDERING_KEYS.PURCHASE_DATE,
    label: SORTING_FIELDS_TRANSLATE.PURCHASE_DATE,
  },
])

const handleSortingUpdate = (val: string | null) => {
  purchasedCoursesStore.setOrdering(val)
}
const handleVisibilityUpdate = (val: boolean) => {
  purchasedCoursesStore.setFilterVisibility(val)
  if (isMobile.value) {
    if (val) {
      document.body.classList.add('fixed-scroll')
    } else {
      document.body.classList.remove('fixed-scroll')
    }
  }
}
const handleSearchInput = async (val: string) => {
  purchasedCoursesStore.setSearch(val)
  await purchasedCoursesStore.loadPurchasedCoursesFilters()
}
const handleFiltersUpdate = async (val: Recordable) => {
  purchasedCoursesStore.setFilters(val)
  await purchasedCoursesStore.loadPurchasedCoursesFilters()
}
const handleFiltersReset = async () => {
  purchasedCoursesStore.resetFilters()
  await purchasedCoursesStore.loadPurchasedCoursesFilters()
  // Clear filter inputs
  if (filterListRef.value) {
    filterListRef.value.checkListRef.forEach((checkList: any) => (checkList.search = ''))
    filterListRef.value.rangeListRef.forEach((rangeList: any) => rangeList.setRangeValues())
  }
}

onMounted(() => {
  purchasedCoursesStore.loadStore()
})

onUnmounted(() => {
  purchasedCoursesStore.clearStore()
})
</script>

<template>
  <div class="text-h5 font-weight-bold d-block d-md-none mb-2">Мои курсы</div>
  <div class="purchased-courses" :class="{ filter: purchasedCoursesStore.isFiltersVisible }">
    <div class="purchased-courses__header">
      <div class="purchased-courses__header-title">
        {{ purchasedCoursesStore.getFilteredTitle }}
      </div>
    </div>

    <div class="purchased-courses__header-filters">
      <BaseTextField
        v-model="purchasedCoursesStore.search"
        label="Поиск"
        prepend-inner-icon="mdi-magnify"
        :debounce="300"
        clearable
        class="purchased-courses__header-search"
        @update:modelValue="handleSearchInput"
      />

      <div
        class="d-flex w-100 w-sm-auto align-center justify-space-between justify-sm-end pa-2 border-mobile ga-4"
      >
        <SortingBar
          :items="sortingItems"
          :is-reversed="xs"
          class="order-1 order-sm-0"
          :ordering="purchasedCoursesStore.ordering"
          @update-sorting="handleSortingUpdate"
        />
        <FilterTrigger
          :filter-visibility="purchasedCoursesStore.isFiltersVisible"
          :is-reversed="xs"
          text="Фильтр"
          :count="purchasedCoursesStore.getActiveFiltersCount"
          @update-visibility="handleVisibilityUpdate"
        />
      </div>
    </div>

    <div class="purchased-courses__main">
      <v-infinite-scroll
        :key="purchasedCoursesStore.renderKey"
        :items="purchasedCoursesStore.infinteLoaderData"
        :onLoad="purchasedCoursesStore.loadOnScroll"
      >
        <div class="purchased-courses__grid">
          <CourseCard
            v-for="course in purchasedCoursesStore.infinteLoaderData"
            :key="course.id"
            :course="course.course"
            class="purchased-courses__card"
          />
        </div>
        <template v-slot:loading>
          <div class="purchased-courses__loader-container">
            <v-progress-circular indeterminate />
          </div>
        </template>
        <template v-slot:empty></template>
      </v-infinite-scroll>

      <Teleport to="header" :disabled="!isMobile">
        <FiltersPanel
          v-if="purchasedCoursesStore.isFiltersVisible"
          :is-mobile="isMobile"
          @reset="handleFiltersReset"
          @update-visibility="handleVisibilityUpdate"
        >
          <CoursesFilters
            v-if="purchasedCoursesStore.getFiltersCatalog"
            ref="filterListRef"
            :filter-catalog="purchasedCoursesStore.getFiltersCatalog"
            :filters="purchasedCoursesStore.filters"
            :filters-update="handleFiltersUpdate"
          />
        </FiltersPanel>
      </Teleport>
    </div>
  </div>
</template>

<style lang="scss">
.purchased-courses {
  display: flex;
  flex-direction: column;
  gap: 16px;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    @include sm() {
      flex-wrap: wrap;
    }
    &-title {
      @include typography('h6');
      @include xs() {
        margin-bottom: 8px;
      }
    }

    &-filters {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 32px;

      @include xs() {
        flex-direction: column;
        gap: 16px;
      }

      &-sort {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      & > button {
        padding: 0;
      }
    }

    &-search {
      max-width: 300px;

      @include xs() {
        max-width: 100%;
        width: 100%;
      }
    }
  }

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
      width: calc(50% - (16px / 3));
    }
    @include sm {
      width: calc(50% - 16px);
    }
  }

  & .v-infinite-scroll__side {
    padding: 0;
  }

  &__main {
    display: flex;
    justify-content: center;
    gap: 32px;
    width: 100%;

    @include md {
      gap: 16px;
    }

    & .filter-container {
      width: calc(33.33% - (32px / 1.5));

      @include md {
        width: calc(50% - (16px / 2));
      }
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

    & .purchased-courses__card {
      height: fit-content !important;
      width: calc(33.33% - (32px / 1.5));
      @include md {
        width: calc(50% - (16px / 2));
      }
      @include xs {
        width: 100%;
      }
    }
  }

  &.filter {
    & .purchased-courses__card {
      width: calc(50% - (32px / 2));
      @include md {
        width: 100%;
      }
    }
    @include xs {
      grid-template-columns: 1fr;
    }
  }

  &__filter {
    position: relative;
    transition: $transition;
    overflow: hidden;
    opacity: 0;
    width: 0;

    &.fade {
      opacity: 1;
      width: auto;
    }
  }
}
.border-mobile {
  @include xs {
    border-radius: 8px;
    border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
  }
}
</style>
