<script setup lang="ts">
import { ref, watch } from 'vue'

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const isDialogOpen = ref(false)

watch(() => isDialogOpen.value, (newVal) => {
  emit('update:modelValue', newVal)  // Обновление значения для v-model
})
</script>

<template>
  <v-dialog :persistent="false" v-model="isDialogOpen" class="pa-0 dialog-blur">
    <v-progress-circular
      indeterminate
      size="168"
      color="rgba(54, 57, 64, 0.8)"
      width="16"
    ></v-progress-circular>
  </v-dialog>
</template>

<style scoped>
.dialog-blur :deep(.v-overlay__scrim) {
  background: rgba(255, 255, 255, 0.40);
  backdrop-filter: blur(12px);
  opacity: 1;
}
.dialog-blur :deep(.v-overlay__content) {
  justify-content: center;
  align-items: center;
}
</style>
