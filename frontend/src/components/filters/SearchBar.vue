<script setup lang="ts">
import { useDebounceFn } from '@vueuse/core'

defineProps<{
  search: string
}>()

const emits = defineEmits<{
  (e: 'updateSearch', val: string): void
}>()

const debouncedSearch = useDebounceFn((search: string) => {
  emits('updateSearch', search)
}, 500)
</script>

<template>
  <v-text-field
    :model-value="search"
    variant="outlined"
    placeholder="Поиск"
    prepend-inner-icon="mdi-magnify"
    rounded="lg"
    clearable
    hide-details
    @update:modelValue="debouncedSearch"
  />
</template>

<style scoped></style>
