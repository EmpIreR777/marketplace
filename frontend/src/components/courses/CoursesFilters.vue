<script setup lang="ts">
import { computed, ref } from 'vue'
import { FILTER_PROPERTIES_NAMES } from '@/api/coursesFilters/constants'
import { FILTER_PROPERTIES_TITLES } from '@/enums/coursesFiltersEnum'
import FilterCheckList from '@/components/filters/FilterCheckList.vue'
import FilterRange from '@/components/filters/FilterRange.vue'
import type { Recordable } from '@/types'
import type { IBaseFilterCatalog } from '@/api/models'
import { RangeFilterEnum } from '@/enums/coursesFiltersEnum'

const props = defineProps<{
  filterCatalog: IBaseFilterCatalog | null
  filters: Recordable
  filtersUpdate: (val: Recordable) => Promise<void>
}>()

const loading = ref(false)
const checkListRef = ref()
const rangeListRef = ref()

defineExpose({
  rangeListRef,
  checkListRef,
})

const sortedFilters = computed(() => {
  const keys = Object.keys(props.filterCatalog ?? {})
  return keys.sort((a, b) => {
    const order = [
      FILTER_PROPERTIES_NAMES.price,
      FILTER_PROPERTIES_NAMES.learning_types,
      FILTER_PROPERTIES_NAMES.organization_type,
    ] as string[]

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
    <FilterRange
      v-if="filter === RangeFilterEnum.PRICE"
      ref="rangeListRef"
      :title="FILTER_PROPERTIES_TITLES[filter]"
      :filter-key="FILTER_PROPERTIES_NAMES[filter] as RangeFilterEnum"
      :range="props.filterCatalog?.[filter]"
      :activeFilters="props.filters"
      :disable="loading"
      @update-range="handleFilterUpdate"
    />

    <FilterCheckList
      v-else
      ref="checkListRef"
      :title="FILTER_PROPERTIES_TITLES[filter as keyof typeof FILTER_PROPERTIES_TITLES]"
      :items="props.filterCatalog?.[filter] || []"
      :filter-key="FILTER_PROPERTIES_NAMES[filter as keyof typeof FILTER_PROPERTIES_NAMES]"
      :activeFilters="props.filters"
      :disable="loading"
      @update-active-checks="handleFilterUpdate"
    />
  </template>
</template>

<style></style>
