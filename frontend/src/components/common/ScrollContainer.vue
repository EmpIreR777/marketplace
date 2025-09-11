<script setup lang="ts">
import {useScrollDrag} from "@/hooks/useScrollDrag.ts";
import type {PropType} from "vue";

defineProps({
  customClasses: {
    type: [String, Array] as PropType<string | string[]>,
    default: ""
  }
});

const { scrollContainer } = useScrollDrag();
</script>

<template>
  <div ref="scrollContainer" :class="['mt-4 mt-sm-15 scroll-container py-1 pl-1', customClasses]">
    <slot></slot>
  </div>
</template>

<style scoped>
.scroll-container {
  display: flex;
  overflow-x: auto;
  flex-wrap: nowrap;
  scrollbar-width: none; /* Убираем полосу прокрутки для Firefox */
}
.scroll-container::-webkit-scrollbar {
  display: none; /* Убираем полосу прокрутки для Chrome/Safari */
}

.scroll-container:hover {
  cursor: grab;
}

.scroll-container:active {
  cursor: grabbing;
}
</style>
