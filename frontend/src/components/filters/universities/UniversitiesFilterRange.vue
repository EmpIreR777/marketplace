<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { Recordable } from '@/types'
import { useDebounceFn } from '@vueuse/core'
import { RangeFilterEnum } from '@/enums/coursesFiltersEnum'

const props = defineProps<{
  title: string
  filterKey: RangeFilterEnum
  range: { min: number; max: number }
  activeFilters: Recordable
  disable: boolean
}>()

const emits = defineEmits<{
  (e: 'updateRange', val: Recordable): void
}>()

const min = ref<number | null>(null)
const max = ref<number | null>(null)

defineExpose({
  setRangeValues,
})

const emitUpdate = useDebounceFn(() => {
  emits('updateRange', {
    [`${props.filterKey}_min`]: min.value,
    [`${props.filterKey}_max`]: max.value,
  })
}, 800)

function updatePriceMin(val: number | null) {
  min.value = val
  emitUpdate()
}

function updatePriceMax(val: number | null) {
  max.value = val
  emitUpdate()
}

function setRangeValues() {
  const range = props.activeFilters[props.filterKey]
  min.value = range?.min ?? null
  max.value = range?.max ?? null
}

onMounted(() => {
  setRangeValues()
})
</script>

<template>
  <div class="d-flex flex-column ga-4">
    <h3 class="text-body-1 font-weight-bold">{{ props.title }}</h3>

    <div v-if="props.range" class="d-flex ga-2">
      <v-number-input
        :model-value="min"
        :min="props.range.min"
        :max="props.range.max"
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
        :model-value="max"
        :min="min ?? props.range.min"
        :max="props.range.max"
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
