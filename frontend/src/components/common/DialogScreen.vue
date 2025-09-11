<script setup lang="ts">
import {ref, watch, onMounted, onUnmounted} from 'vue'

// Определяем событие с помощью defineEmits
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const isDialogOpen = ref(false)

watch(() => isDialogOpen.value, (newVal) => {
  emit('update:modelValue', newVal)  // Обновление значения для v-model
})
const closeDialog = () => {
  emit('update:modelValue', false)
}
const handleEsc = (event: KeyboardEvent) => {
  if (event.key === 'Escape') closeDialog()
}

onMounted(() => window.addEventListener('keydown', handleEsc))
onUnmounted(() => window.removeEventListener('keydown', handleEsc))


</script>

<template>
  <v-dialog :persistent="false" v-model="isDialogOpen" class="pa-0 dialog-blur">
    <slot></slot>
  </v-dialog>
</template>

<style scoped>
.dialog-blur :deep(.v-overlay__scrim) {
  background: rgba(255, 255, 255, 0.40);
  backdrop-filter: blur(12px);
  opacity: 1;
}
</style>
