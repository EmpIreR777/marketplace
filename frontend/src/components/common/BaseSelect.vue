<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: string
  items: any[]
}>()

const emits = defineEmits(['update:modelValue'])

const inputValue = ref(props.modelValue)

watch(
  () => props.modelValue,
  (newValue) => {
    inputValue.value = newValue
  },
)

watch(inputValue, (newValue) => {
  emits('update:modelValue', newValue)
})
</script>

<template>
  <div class="base-filter-menu">
    <v-select v-model="inputValue" :items="props.items" hide-details></v-select>
  </div>
</template>

<style lang="scss">
.base-filter-menu {
  border: 1px solid $base-20;
  border-radius: 12px;

  & .v-field {
    padding-right: 0;

    &__append-inner {
      padding-right: 16px;
    }

    &__overlay {
      background-color: transparent;
    }

    &__outline {
      display: none;
    }
  }
}
</style>
