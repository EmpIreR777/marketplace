<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import type { Recordable } from '@/types'
import { FILTER_CHECKBOX_VISIBLE_COUNT } from '@/enums/coursesFiltersEnum'
import type { FILTER_PROPERTIES_NAMES } from '@/api/coursesFilters/constants'
import type { IOption } from '@/api/models'

const props = defineProps<{
  title: string
  searchLabel?: string
  items: IOption[]
  itemsVisibleCount?: number
  filterKey: keyof typeof FILTER_PROPERTIES_NAMES
  activeFilters: Recordable
  disable: boolean
}>()

const emits = defineEmits<{
  (e: 'updateActiveChecks', val: Recordable): void
}>()

const search = ref<string | null>(null)
const showAll = ref<boolean>(false)

defineExpose({
  search,
})

const visibleCount = computed(() => props.itemsVisibleCount ?? FILTER_CHECKBOX_VISIBLE_COUNT)

const filteredItems = computed(() => {
  let items = [...props.items]

  if (search.value) {
    const searchTerm = search.value.trim().toLowerCase()

    items = items.filter((item) => {
      const { name, translations } = item
      return [name, ...(translations ? [translations] : [])].some((i) =>
        i.toLowerCase().includes(searchTerm),
      )
    })
  }

  return items
})

const visibleItems = computed(() => {
  const sortedItems = [...filteredItems.value].sort((it1, it2) => {
    const index1 = selectedValues.value.indexOf(it1.name)
    const index2 = selectedValues.value.indexOf(it2.name)

    if (index1 !== -1 && index2 !== -1) {
      return index1 - index2
    }
    if (index1 !== -1) return -1
    if (index2 !== -1) return 1
    return 0
  })

  return showAll.value ? sortedItems : sortedItems.slice(0, visibleCount.value)
})

const totalItems = computed(() => filteredItems.value.length)

const selectedValues = ref<string[]>([])

function handleCheckboxInput(selectedItem: string) {
  const index = selectedValues.value.indexOf(selectedItem)
  if (index > -1) {
    selectedValues.value.splice(index, 1)
  } else {
    selectedValues.value.push(selectedItem)
  }
  emits('updateActiveChecks', { [props.filterKey]: [...selectedValues.value] })
}

function syncSelectedValues() {
  const val = props.activeFilters[props.filterKey]

  if (Array.isArray(val)) {
    selectedValues.value = [...val]
  } else if (typeof val === 'string') {
    selectedValues.value = [val]
  } else {
    selectedValues.value = []
  }
}

watchEffect(syncSelectedValues)
</script>

<template>
  <div v-if="items.length" class="d-flex flex-column ga-4">
    <h3 class="text-body-1 font-weight-bold">{{ title }}</h3>

    <v-text-field
      v-if="items.length > visibleCount"
      v-model="search"
      :label="searchLabel ?? 'Поиск'"
      variant="outlined"
      clearable
      rounded="lg"
      prepend-inner-icon="mdi-magnify"
    />

    <v-list class="pa-0">
      <v-list-item v-for="item in visibleItems" :key="item.name" class="mb-1">
        <v-checkbox
          class="custom-checkbox"
          density="compact"
          :model-value="selectedValues"
          :label="item.translations && item.translations.length ? item.translations : item.name"
          :value="item.name"
          :disabled="props.disable"
          @update:modelValue="handleCheckboxInput(item.name)"
        />
      </v-list-item>
    </v-list>

    <v-btn
      v-if="totalItems > visibleCount"
      class="show-all"
      variant="text"
      @click="showAll = !showAll"
    >
      {{ showAll ? 'Скрыть' : `Показать все ${totalItems}` }}
    </v-btn>
  </div>
</template>

<style scoped>
.content-wrapper {
  max-height: 600px;
  overflow-y: auto;
}

.custom-checkbox {
  color: var(--Base-color-80, rgba(54, 57, 64, 0.8));
}

.show-all {
  text-transform: none;
  font-size: 16px;
  font-weight: 300;
  line-height: 24px; /* 150% */
  padding-left: 0;
  color: var(--Base-color-80, rgba(54, 57, 64, 0.8));
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: none;
  text-decoration-thickness: 7.5%; /* 1.2px */
  text-underline-offset: 15%; /* 2.4px */
  text-underline-position: from-font;
}

::v-deep(.v-list-item) {
  padding: 0 !important;
  margin-top: -4px !important;
}

::v-deep(.v-label) {
  margin-left: 8px;
  line-height: 1.3;
}

::v-deep(.v-input__details) {
  display: none;
}
</style>
