<script setup lang="ts">
import { ref, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'

const props = defineProps<{
  modelValue: string
  label?: string
  prependInnerIcon?: string
  debounce?: number
  clearable?: boolean
}>()

const emits = defineEmits(['update:modelValue'])

const inputValue = ref(props.modelValue)

const emitUpdate = (value: string) => {
  emits('update:modelValue', value)
}

const debouncedEmitUpdate = props.debounce
? useDebounceFn(emitUpdate, props.debounce)
: emitUpdate

watch(
  () => props.modelValue,
  (newValue) => {
    inputValue.value = newValue
  },
)

watch(inputValue, (newValue) => {
  debouncedEmitUpdate(newValue)
})
</script>

<template>
  <v-text-field
    v-model="inputValue"
    :label="props.label"
    class="base-text-field"
    :prepend-inner-icon="props.prependInnerIcon"
    :clearable="props.clearable"
    hide-details
  ></v-text-field>
</template>

<style lang="scss">
.base-text-field {
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
