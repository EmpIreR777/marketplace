<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: boolean
}>()

const switchValue = ref(props.modelValue)

const emits = defineEmits(['update:modelValue'])

watch(
  () => props.modelValue,
  (newValue) => {
    switchValue.value = newValue
  },
)

watch(switchValue, (newValue) => {
  emits('update:modelValue', newValue)
})
</script>

<template>
  <v-switch class="base-switch" v-model="switchValue" hide-details inset :ripple="false"></v-switch>
</template>

<style lang="scss">
.base-switch {
  & .v-switch__track {
    border: 2px solid $base;
    background-color: transparent;
    opacity: 1;
    height: 14px;
    width: 24px;
    min-width: 24px;
  }

  & .v-selection-control {
    height: 24px;
    min-height: 24px;

    &__wrapper {
      height: 24px;
    }

    &__input::before {
      content: none;
    }
  }

  & .v-switch__thumb {
    border: 2px solid $base;
    height: 6px;
    width: 6px;
    transform: scale(1) translateX(6px);
  }

  & .v-selection-control--dirty {
    & .v-switch__thumb {
      transform: scale(1) translateX(-6px);
    }
  }
}
</style>
