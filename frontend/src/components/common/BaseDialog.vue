<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import BaseButton from './BaseButton.vue'

withDefaults(
  defineProps<{
    modelValue: boolean
    title: string
    text?: string
    confirmText: string
    cancelText: string
    width?: string
    persistent?: boolean
    isconfirmDisabled?: boolean
  }>(),
  {
    width: '500px',
    persistent: false,
  },
)

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

// Закрытие диалога
const closeDialog = () => emit('update:modelValue', false)
const confirmAction = () => {
  emit('confirm')
  closeDialog()
}
const cancelAction = () => {
  emit('cancel')
  closeDialog()
}
</script>

<template>
  <v-dialog :model-value="modelValue" :width="width" :persistent="persistent" class="base-dialog">
    <v-card elevation="0" class="base-dialog__card rounded-lg">
      <!-- Заголовок -->
      <v-card-title class="base-dialog__title">
        {{ title }}
      </v-card-title>

      <!-- Основной текст -->
      <v-card-text v-if="text">
        <span class="base-dialog__text">{{ text }}</span>
      </v-card-text>

      <!-- Слот для кастомного контента -->
      <v-card-text v-else>
        <span class="base-dialog__text"><slot /></span>
      </v-card-text>

      <!-- Кнопки -->
      <v-card-actions class="base-dialog__actions">
        <BaseButton v-if="cancelText" :label="cancelText" type="outline" @click="cancelAction" />
        <BaseButton
          v-if="confirmText"
          :label="confirmText"
          :disabled="!!isconfirmDisabled"
          @click="confirmAction"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style lang="scss">
.base-dialog {
  &__card {
    border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
  }

  &__title {
    @include typography('h5');
    padding: 24px 24px 0;

    @include sm {
      @include typography('h6');
    }
  }

  & .v-card-text {
    padding: 16px 24px 0 !important;
  }

  &__text {
    @include typography('lg');
  }

  &__actions {
    display: flex;
    gap: 16px;
    padding: 40px 24px 24px;

    & > button {
      flex: 1;
    }
  }

  .v-overlay__scrim {
    background: rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(12px);
    opacity: 1;
  }
}
</style>
