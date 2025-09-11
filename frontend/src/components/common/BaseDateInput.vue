<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: Date | Date[] | null
  icon?: boolean
  isMultiple?: boolean | 'range'
  label?: string
}>()

const inputValue = ref(props.modelValue)

const emits = defineEmits(['update:modelValue'])

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
  <div class="base-date-input">
    <v-date-input
      v-model="inputValue"
      :multiple="isMultiple"
      prepend-icon=""
      :append-inner-icon="props.icon ? 'mdi-calendar' : ''"
      :persistent-placeholder="!label"
      :label
      hide-details
    ></v-date-input>
  </div>
</template>

<style lang="scss">
.base-date-input {
  min-width: 150px;
  color: $base-60;

  & .v-field {
    border-radius: 12px;
    border: 1px solid $base-20;

    &__overlay {
      background-color: transparent;
    }

    &__outline {
      display: none;
    }
  }
}
</style>
