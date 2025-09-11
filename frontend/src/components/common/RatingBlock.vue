<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { emptyStarIcon, fullStarIcon } from '@/assets/icons'

const props = withDefaults(
  defineProps<{
    rating: number
    showValue: boolean
    classes?: string
  }>(),
  {
    classes: '',
  },
)

const emit = defineEmits<{
  (e: 'update:rating', value: number): void
}>()

// Локальный рейтинг, если `rating` не передан
const localRating = ref<number>(props.rating ?? 0)

// Следим за изменением пропа `rating` и обновляем локальное состояние
watch(
  () => props.rating,
  (newRating) => {
    if (newRating !== undefined) {
      localRating.value = newRating
    }
  },
)

// Вычисляемый рейтинг
const displayedRating = computed(() => props.rating ?? localRating.value)

// Обработчик клика: обновляет локальный рейтинг и эмитит новое значение
const setRating = (index: number) => {
  if (props.rating === undefined) {
    localRating.value = index + 1
  }
  emit('update:rating', index + 1)
}
</script>

<template>
  <div :class="props.classes" class="rating-container">
    <img
      v-for="index in 5"
      :key="index"
      :src="index <= displayedRating ? fullStarIcon : emptyStarIcon"
      alt="Star Icon"
      class="rating-icon"
      :class="{ clickable: true }"
      @click="setRating(index - 1)"
    />
    <span v-if="props.showValue" class="rating-value">{{ props.rating }}</span>
  </div>
</template>

<style scoped lang="scss">
.rating-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  line-height: 1;

  @media (max-width: 1279px) {
    justify-content: center;
  }
}

.rating-icon {
  display: inline-block;
  width: 24px;
  height: 24px;
}

.rating-value {
  display: inline-block;
  font-size: 1rem;
  font-weight: 700;

  @include sm {
    font-size: 0.75rem;
  }
}

.clickable {
  cursor: pointer;
}
</style>
