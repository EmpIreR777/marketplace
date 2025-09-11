<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { Recordable } from '@/types'
import { FILTER_PROPERTIES_TITLES } from '@/enums/coursesFiltersEnum'
import BaseTextField from '@/components/common/BaseTextField.vue'
import { useUniversitiesStore } from '@/stores/Universities'
import type { IOption } from '@/api/models'

const props = defineProps<{
  filterKey: keyof typeof FILTER_PROPERTIES_TITLES
  items: IOption[]
  total: number
  totalSearch: number
  selectedItems: string[]
  disable: boolean
}>()

const emits = defineEmits<{
  (e: 'updateActiveChecks', val: Recordable): void
}>()

const limit = 10
const universitiesStore = useUniversitiesStore()
const search = ref('')
const offset = ref(limit)
const selectedValues = ref<string[]>(props.selectedItems)

defineExpose({
  search,
})

const hasShowMoreBtn = computed(() => props.totalSearch > limit && props.totalSearch > offset.value)
const showMoreBtnCount = computed(() =>
  props.totalSearch >= offset.value + limit ? limit : props.totalSearch - offset.value,
)

async function handleSearchInput() {
  offset.value = 0

  await universitiesStore.loadUniversitiesFilterByInnerSearch(
    search.value.trim(),
    props.filterKey,
    offset.value,
  )

  offset.value += limit
}

function handleCheckboxInput(selectedItem: string) {
  const index = selectedValues.value.indexOf(selectedItem)
  if (index > -1) {
    selectedValues.value.splice(index, 1)
  } else {
    selectedValues.value.push(selectedItem)
  }
  emits('updateActiveChecks', { [props.filterKey]: [...selectedValues.value] })
}

async function showMore() {
  await universitiesStore.loadUniversitiesFilterByInnerSearch(
    search.value.trim(),
    props.filterKey,
    offset.value,
    true,
  )

  offset.value += limit
}

watch(
  () => props.selectedItems,
  (newVal) => {
    selectedValues.value = [...newVal]
  },
)
</script>

<template>
  <div class="d-flex flex-column ga-2">
    <h3 class="text-body-1 font-weight-bold">
      {{ FILTER_PROPERTIES_TITLES[props.filterKey] }}
    </h3>

    <BaseTextField
      v-if="props.total > 10"
      v-model="search"
      label="Поиск"
      prepend-inner-icon="mdi-magnify"
      :debounce="800"
      @update:modelValue="handleSearchInput"
    />

    <v-list class="pa-0">
      <v-list-item v-for="item of props.items" :key="item.id">
        <v-checkbox
          :model-value="selectedValues"
          density="compact"
          :label="item.name"
          :value="item.name"
          :disabled="props.disable"
          class="custom-checkbox"
          @update:modelValue="handleCheckboxInput(item.name)"
        />
      </v-list-item>
    </v-list>

    <v-btn v-if="hasShowMoreBtn" variant="text" class="show-all" @click="showMore">
      Показать ещё {{ showMoreBtnCount }}
    </v-btn>
  </div>
</template>

<style lang="scss" scoped>
.content-wrapper {
  max-height: 600px;
  overflow-y: auto;
}

.custom-checkbox {
  color: $base-80;
}

.show-all {
  @include typography('lg');
  color: $base-80;
  text-transform: none;
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: none;
  text-decoration-thickness: 7.5%;
  text-underline-offset: 15%;
  text-underline-position: from-font;
  width: fit-content;
}

::v-deep(.v-list-item) {
  padding: 0 !important;
  min-height: 40px;
}

::v-deep(.v-label) {
  margin-left: 8px;
  line-height: 1.3;
}

::v-deep(.v-input__details) {
  display: none;
}
</style>
