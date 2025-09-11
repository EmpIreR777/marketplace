<script setup lang="ts">
import { ref, watch } from 'vue'
import { useCoursesStore } from '@/stores/Courses'
import { useDebounceFn } from '@vueuse/core'

const emit = defineEmits<{
  (e: 'update:selected', data: { selectedValues: string[]; title: string }): void
}>()

const props = defineProps<{
  title: string
  filterKey: string
  min: string | null
  max: string | null
  reset?: boolean
}>()

const coursesStore = useCoursesStore()
const minValue = ref<string | null>(props.min)
const maxValue = ref<string | null>(props.max)

function validatePositiveNumbers(event: KeyboardEvent) {
  const char = event.key

  if (!/^\d$/.test(char)) {
    event.preventDefault()
  }
}

const emitUpdate = () => {
  emit('update:selected', {
    selectedValues: [minValue.value ?? '', maxValue.value ?? ''],
    title: props.filterKey,
  })
  coursesStore.clearCourses()
}

const emitUpdateDebounced = useDebounceFn(emitUpdate, 300)

watch([minValue, maxValue], () => {
  emitUpdateDebounced()
})

watch(
  () => props.min,
  (newMin) => {
    minValue.value = newMin
  },
)

watch(
  () => props.max,
  (newMax) => {
    maxValue.value = newMax
  },
)
</script>

<template>
  <v-container fluid class="pa-0">
    <h3 class="block-title">{{ title }}</h3>

    <v-row>
      <v-col>
        <v-text-field
          v-model.number="minValue"
          variant="outlined"
          class="mt-4"
          rounded="lg"
          min="0"
          type="number"
          @keypress="validatePositiveNumbers"
        />
      </v-col>
      <v-col>
        <v-text-field
          v-model.number="maxValue"
          variant="outlined"
          class="mt-4"
          rounded="lg"
          min="0"
          type="number"
          @keypress="validatePositiveNumbers"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
