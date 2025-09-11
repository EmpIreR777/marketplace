<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useDisplay } from 'vuetify'

const props = defineProps<{
  ordering?: string | null
  items: any[]
  isReversed?: boolean
}>()

const emits = defineEmits<{
  (e: 'updateSorting', val: string | null): void
}>()

const { xs } = useDisplay()

const selectedSort = ref<string | null>(null)
const isDescending = ref<boolean>(false)

watch(
  () => props.ordering,
  (newOrdering) => {
    selectedSort.value = newOrdering ? newOrdering.replace(/^-/, '') : null
    isDescending.value = newOrdering ? newOrdering.startsWith('-') : false
  },
  { immediate: true },
)

const updateSorting = () => {
  const val = selectedSort.value ? `${isDescending.value ? '-' : ''}${selectedSort.value}` : null
  emits('updateSorting', val)
}

const selectSorting = (val: string | null) => {
  selectedSort.value = val
  if (!val) isDescending.value = false
  updateSorting()
}

const toggleSortingDirection = () => {
  if (selectedSort.value) {
    isDescending.value = !isDescending.value
    updateSorting()
  }
}

const selectedLabel = computed(() => {
  if (!selectedSort.value) return 'Сортировка'
  const selectedItem = props.items.find((item) => item.apiKey === selectedSort.value)
  return selectedItem?.label ?? 'Сортировка'
})
</script>
<template>
  <div class="d-flex align-center ga-1 ga-sm-2">
    <v-menu end>
      <template #activator="{ props: menuProps }">
        <v-btn
          v-bind="menuProps"
          variant="text"
          class="menu-sort-button"
          :class="isReversed ? 'order-1 justify-start text-start' : 'justify-end text-end'"
        >
          <span class="d-flex flex-column">
            <span class="txt">{{ xs ? 'Сортировка' : selectedLabel }}</span>
            <span class="descr d-sm-none">
              {{ selectedLabel }}
            </span>
          </span>
        </v-btn>
      </template>

      <v-list class="select-menu">
        <v-list-item value="null" subtitle="Очистить" @click="selectSorting(null)" />
        <v-list-item
          v-for="item in items"
          :key="item.apiKey"
          :value="item.apiKey"
          @click="selectSorting(item.apiKey)"
        >
          {{ item.label }}
        </v-list-item>
      </v-list>
    </v-menu>

    <v-btn :size="xs ? 18 : 24" variant="text" @click="toggleSortingDirection">
      <v-icon
        :size="xs ? 18 : 24"
        :icon="isDescending ? 'mdi-sort-descending' : 'mdi-sort-ascending'"
      />
    </v-btn>
  </div>
</template>

<style scoped lang="scss">
.select-menu {
  min-width: 240px;
  border-radius: 12px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
  background: var(--White-color-100, #fff);
}

.menu-sort-button {
  text-transform: none;
  font-weight: 400;
  justify-content: end;
}

.direction-sort-button {
  min-width: 24px;
  width: 24px;
  height: 24px;
  padding: 0;
}

.direction-sort-button__img {
  transition: transform 0.3s ease; /* Smooth transition */
}

.rotated {
  transform: rotate(180deg);
  transition: transform 0.3s ease; /* Smooth transition */
}

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
