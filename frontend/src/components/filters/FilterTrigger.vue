<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'

const props = defineProps<{
  filterVisibility: boolean
  text?: string
  count?: number
  isReversed?: boolean
}>()

const emits = defineEmits<{
  (e: 'updateVisibility', val: boolean): void
}>()

const { xs } = useDisplay()

const descr = computed(() =>
  props.count && props.count > 0 ? `Выбрано ${props.count}` : 'Не выбран',
)

const toggleFilterVisibility = () => {
  emits('updateVisibility', !props.filterVisibility)
}
</script>

<template>
  <v-btn variant="text" style="text-transform: none" @click="toggleFilterVisibility">
    <span class="d-inline-flex align-center ga-1 ga-sm-2">
      <span
        v-if="text"
        class="d-inline-flex flex-column"
        :class="isReversed ? 'order-1 justify-start text-start' : 'justify-end text-end'"
      >
        <span class="txt">{{ text }}</span>
        <span class="descr d-sm-none">
          {{ descr }}
        </span>
      </span>
      <v-icon icon="mdi-filter-outline" :size="xs ? 18 : 24"></v-icon>
    </span>
  </v-btn>
</template>

<style scoped lang="scss">
.txt {
  line-height: 1;
  @include typography('lg');
  @include xs {
    @include typography('mdb');
  }
}

.descr {
  line-height: 1;
  @include typography('md');
  @include xs {
    @include typography('sm');
  }
}
</style>
