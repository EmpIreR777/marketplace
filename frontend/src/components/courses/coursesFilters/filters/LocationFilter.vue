<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from "vue";

const props = defineProps<{
  label?: string;
  reset: boolean;
}>();

const emit = defineEmits<{
  (e: "update:selected", data: { selectedValues: string[]; title: string }): void;
}>();

const location = ref("");
let timeout: ReturnType<typeof setTimeout> | null = null;

// Следим за вводом в `location`, но эмитим только после паузы 2 секунды
watch(location, (newSelected) => {
  if (timeout) clearTimeout(timeout); // Сброс старого таймера

  timeout = setTimeout(() => {
    emit("update:selected", { selectedValues: newSelected ? [newSelected] : [], title: "Местоположение" });
  }, 2000);
});

// Сбрасываем поле при `reset = true`
watch(
  () => props.reset,
  (newValue) => {
    if (newValue) {
      location.value = "";
      if (timeout) clearTimeout(timeout); // Очищаем таймер при сбросе
    }
  }
);

// Очистка таймера при удалении компонента
onBeforeUnmount(() => {
  if (timeout) clearTimeout(timeout);
});
</script>

<template>
  <v-container fluid class="pa-0 mt-6">
    <h3 class="block-title">Регион</h3>

    <v-text-field
      v-model="location"
      label="Местоположение"
      variant="outlined"
      class="mt-4"
      rounded="lg"
      append-inner-icon="mdi-crosshairs-gps"
    />
  </v-container>
</template>

<style scoped></style>
