<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Recordable } from '@/types'
import type { IUniversitiesFilterCatalog } from '@/api/models'
import UniversitiesCheckList from '@/components/filters/universities/UniversitiesCheckList.vue'
import { useUniversitiesStore } from '@/stores/Universities'
import UniversitiesFilterRange from '@/components/filters/universities/UniversitiesFilterRange.vue'
import { FILTER_PROPERTIES_NAMES } from '@/api/coursesFilters/constants'
import { FILTER_PROPERTIES_TITLES, RangeFilterEnum } from '@/enums/coursesFiltersEnum'

const props = defineProps<{
  filterCatalog: IUniversitiesFilterCatalog
  filters: Recordable
  filtersUpdate: (val: Recordable) => Promise<void>
}>()

const loading = ref(false)
const universitiesStore = useUniversitiesStore()
const checkListRef = ref()
const rangeListRef = ref()

defineExpose({
  rangeListRef,
  checkListRef,
})

const sortedFilters = computed(() => {
  const keys = Object.keys(props.filterCatalog ?? {})
  return keys.sort((a, b) => {
    const order = [FILTER_PROPERTIES_NAMES.price, FILTER_PROPERTIES_NAMES.organization_type] as string[]
    const indexA = order.indexOf(a)
    const indexB = order.indexOf(b)

    if (indexA !== -1 && indexB !== -1) {
      return indexA - indexB
    }

    if (indexA !== -1) return -1
    if (indexB !== -1) return 1

    return 0
  })
})

async function handleFilterUpdate(val: Recordable) {
  loading.value = true

  try {
    await props.filtersUpdate(val)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <template v-for="filter in sortedFilters" :key="filter">
    <UniversitiesFilterRange
      v-if="universitiesStore.isRangeFilter(filter)"
      ref="rangeListRef"
      :title="FILTER_PROPERTIES_TITLES[filter as keyof typeof FILTER_PROPERTIES_TITLES]"
      :filter-key="
        FILTER_PROPERTIES_NAMES[filter as keyof typeof FILTER_PROPERTIES_NAMES] as RangeFilterEnum
      "
      :range="props.filterCatalog?.[filter]"
      :activeFilters="props.filters"
      :disable="loading"
      @update-range="handleFilterUpdate"
    />
    <UniversitiesCheckList
      v-else
      ref="checkListRef"
      :filter-key="filter"
      :items="props.filterCatalog[filter].items || []"
      :total="props.filterCatalog[filter].total || 0"
      :total-search="props.filterCatalog[filter].total_search || 0"
      :selected-items="props.filters[filter] || []"
      :disable="loading"
      @update-active-checks="handleFilterUpdate"
    />
  </template>
</template>

<style></style>
