<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { Recordable } from '@/types'
import { FILTER_PROPERTIES_NAMES } from '@/api/coursesFilters/constants'
import type { IPriceRange } from '@/api/coursesFilters/models'
import { useDebounceFn } from '@vueuse/core'

const props = defineProps<{
  title: string
  filterKey: keyof typeof FILTER_PROPERTIES_NAMES
  range?: IPriceRange
  activeFilters: Recordable
  disable: boolean
}>()

const emits = defineEmits<{
  (e: 'updateRange', val: Recordable): void
}>()

const price_min = ref<number | null>(null)
const price_max = ref<number | null>(null)

defineExpose({
  setRangeValues,
})

const emitUpdate = useDebounceFn(() => {
  emits('updateRange', {
    [FILTER_PROPERTIES_NAMES.price_min]: price_min.value,
    [FILTER_PROPERTIES_NAMES.price_max]: price_max.value,
  })
}, 800)

function updatePriceMin(val: number | null) {
  price_min.value = val
  emitUpdate()
}

function updatePriceMax(val: number | null) {
  price_max.value = val
  emitUpdate()
}

function setRangeValues() {
  const range = props.activeFilters[props.filterKey]

  // if (props.activeFilters[FILTER_PROPERTIES_NAMES.price_min]) {
  //   price_min.value =
  //     parseInt(props.activeFilters[FILTER_PROPERTIES_NAMES.price_min]) ?? props.range?.price_min
  // } else {
  price_min.value = range?.price_min ?? null
  // }
  // if (props.activeFilters[FILTER_PROPERTIES_NAMES.price_max]) {
  //   price_max.value =
  //     parseInt(props.activeFilters[FILTER_PROPERTIES_NAMES.price_max]) ?? props.range?.price_max
  // } else {
  price_max.value = range?.price_max ?? null
  // }
}

onMounted(() => {
  setRangeValues()
})
</script>

<template>
  <div class="d-flex flex-column ga-4">
    <h3 class="text-body-1 font-weight-bold">{{ props.title }}</h3>

    <div class="d-flex ga-2">
      <v-number-input
        :model-value="price_min"
        :min="props.range?.price_min"
        :max="props.range?.price_max"
        label="min"
        variant="outlined"
        clearable
        controlVariant="hidden"
        density="comfortable"
        inset
        rounded="lg"
        hide-details
        :disabled="props.disable"
        class="w-50"
        @update:model-value="updatePriceMin"
      />

      <v-number-input
        :model-value="price_max"
        :min="price_min ?? props.range?.price_min"
        :max="props.range?.price_max"
        label="max"
        variant="outlined"
        clearable
        controlVariant="hidden"
        density="comfortable"
        inset
        rounded="lg"
        hide-details
        :disabled="props.disable"
        class="w-50"
        @update:model-value="updatePriceMax"
      />
    </div>
  </div>
</template>

<style scoped></style>
