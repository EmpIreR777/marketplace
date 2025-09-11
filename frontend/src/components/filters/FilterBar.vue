<script setup lang="ts">
import SearchBar from '@/components/filters/SearchBar.vue'
import SortingBar from '@/components/filters/SortingBar.vue'
import FilterTrigger from '@/components/filters/FilterTrigger.vue'
import { API_ORDERING_KEYS, SORTING_FIELDS_TRANSLATE } from '@/enums/coursesFiltersEnum'
import { computed } from 'vue'
import { useDisplay } from 'vuetify'

defineProps<{
  search: string
  sorting: string | null
  activeFiltersCount: number
  filterVisibility: boolean
}>()

const emits = defineEmits<{
  (e: 'updateSearch', val: string): void
  (e: 'updateSorting', val: string | null): void
  (e: 'updateFiltersVisibility', val: boolean): void
}>()

const { xs } = useDisplay()

const sortingItems = computed(() => [
  {
    apiKey: API_ORDERING_KEYS.POPULARITY,
    label: SORTING_FIELDS_TRANSLATE.POPULARITY,
  },
  {
    apiKey: API_ORDERING_KEYS.RATING,
    label: SORTING_FIELDS_TRANSLATE.RATING,
  },
])

const handleSearchUpdate = (val: string) => {
  emits('updateSearch', val)
}
const handleSortingUpdate = (val: string | null) => {
  emits('updateSorting', val)
}
const handleVisibilityUpdate = (val: boolean) => {
  emits('updateFiltersVisibility', val)
}
</script>

<template>
  <div class="d-flex justify-space-between align-center">
    <SearchBar
      :search="search"
      class="d-none d-sm-block"
      max-width="300"
      @update-search="handleSearchUpdate"
    />

    <div
      class="d-flex w-100 w-sm-auto align-center justify-space-between justify-sm-end pa-2 border-mobile ga-4"
    >
      <SortingBar
        :items="sortingItems"
        class="order-1 order-sm-0"
        :ordering="sorting"
        :is-reversed="xs"
        @update-sorting="handleSortingUpdate"
      />

      <FilterTrigger
        :filter-visibility="filterVisibility"
        text="Фильтр"
        :count="activeFiltersCount"
        :is-reversed="xs"
        @update-visibility="handleVisibilityUpdate"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.border-mobile {
  @include xs {
    border-radius: 8px;
    border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
  }
}
</style>
