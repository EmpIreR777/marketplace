<script setup lang="ts">
import BaseButton from '@/components/common/BaseButton.vue'

defineProps<{
  isMobile: boolean
}>()

const emits = defineEmits<{
  (e: 'reset'): void
  (e: 'updateVisibility', val: boolean): void
}>()

const hideFilters = () => {
  emits('updateVisibility', false)
}
</script>

<template>
  <v-card
    elevation="0"
    class="overflow-y-auto filter-container"
    :class="isMobile ? 'filterFixed position-fixed' : 'position-relative'"
  >
    <v-card-text class="pa-0 ga-6" style="display: grid; grid-template-columns: 100%">
      <div class="filter-container__header">
        <v-btn v-if="isMobile" size="32" variant="plain" @click="hideFilters">
          <v-icon size="24">mdi-close</v-icon>
        </v-btn>

        <BaseButton class="reset" type="flat" label="Сбросить" @click="emits('reset')" />
      </div>
      <slot></slot>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss">
.filter-container {
  border-radius: 16px;
  border: 1px solid $base-20;
  height: fit-content;
  padding: 24px;

  @include sm {
    border: none;
    padding: 16px;
    border-radius: 0;
  }

  &__header {
    display: flex;
    align-items: center;
  }
}

.reset {
  margin-left: auto;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.5;
  color: $base-60;
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: none;
  text-decoration-thickness: 7.5%; /* 1.2px */
  text-underline-offset: 15%; /* 2.4px */
  text-underline-position: from-font;
}

.filterFixed {
  height: 100vh;
  padding: 16px 16px 128px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  overflow: auto;
}
</style>
