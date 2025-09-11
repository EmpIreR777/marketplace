<script setup lang="ts">
import { ref, watch } from "vue";
import RatingBlock from "@/components/common/RatingBlock.vue";

const props = defineProps<{
  reset: boolean;
}>();
// Локальное состояние рейтинга
const rating = ref<number>(0);

const emit = defineEmits<{
  (e: "update:selected", data: { selectedValues: string[]; title: string }): void;
}>();

// Следим за изменением рейтинга и эмитируем событие
watch(rating, (newRating) => {
  emit("update:selected", { selectedValues: [String(newRating)], title: "Минимальный рейтинг" });
});

watch(() => props.reset, (newValue) => {
  if (newValue) {
    rating.value = 0;
  }
});
</script>

<template>
  <v-container fluid class="pa-0 mt-3">
    <h3 class="block-title">Минимальный рейтинг</h3>
    <RatingBlock :reset="reset" v-model:rating="rating" classes="mt-2" />
  </v-container>
</template>

<style scoped>
.block-title {
  font-size: 16px;
  font-weight: 700;
  line-height: 24px; /* 150% */
}
</style>

