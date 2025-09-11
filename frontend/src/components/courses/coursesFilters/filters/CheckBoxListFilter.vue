<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCoursesFilterStore } from '@/stores/CoursesFilter'
import { useDisplay } from 'vuetify'
import { AppColors } from '@/enums/appColors'
import type { IOption } from '@/api/models'
import { useCoursesStore } from '@/stores/Courses'

const props = defineProps<{
  title: string
  filterKey: string
  label?: string
  numberCheckboxes: number
  dataCheckbox: IOption[]
  // reset: boolean;
}>()

const coursesFilterStore = useCoursesFilterStore()
const coursesStore = useCoursesStore()
const { xs } = useDisplay()
const search = ref('')
const showAll = ref(false)

// Фильтрация элементов на основе текста поиска
const filteredItems = computed(() => {
  const filtered = props.dataCheckbox.filter((item) =>
    item.translations.toLowerCase().includes(search.value.toLowerCase()),
  )
  return showAll.value ? filtered : filtered.slice(0, props.numberCheckboxes)
})

const totalItems = computed(() => props.dataCheckbox.length)
const { filterKey } = props

async function handleCheckboxInput(selectedItem: string) {
  const selectedValues = coursesFilterStore.getSelectedFilters?.[filterKey] as string[]

  let newValues: string[] = []
  if (Array.isArray(selectedValues)) {
    if ((selectedValues as string[])?.includes(selectedItem)) {
      newValues = selectedValues.filter((v) => v !== selectedItem)
    } else {
      newValues = [...selectedValues, selectedItem]
    }
  } else {
    newValues = [selectedItem]
  }
  coursesFilterStore.setSelectedFilters({ [filterKey]: [...newValues] })
  await coursesFilterStore.loadCoursesFilters()
  coursesStore.clearCourses()
}
</script>

<template>
  <v-container fluid class="pa-0">
    <h3 class="block-title">{{ title }}</h3>

    <v-text-field
      v-if="label"
      v-model="search"
      :label="label"
      variant="outlined"
      :bg-color="xs ? AppColors.BG : undefined"
      class="mt-4"
      rounded="lg"
      prepend-inner-icon="mdi-magnify"
    />

    <v-list>
      <v-list-item v-for="item in filteredItems" :key="item.name" class="mb-1">
        <!-- v-model="selected" -->
        <v-checkbox
          class="custom-checkbox"
          density="compact"
          :model-value="coursesFilterStore.getSelectedFilters?.[filterKey]"
          :label="item.translations.length ? item.translations : item.name"
          :value="item.name"
          @update:modelValue="handleCheckboxInput(item.name)"
        />
      </v-list-item>
    </v-list>

    <v-btn
      v-if="totalItems > props.numberCheckboxes"
      class="show-all"
      variant="text"
      @click="showAll = !showAll"
    >
      {{ showAll ? 'Скрыть' : `Показать все ${totalItems}` }}
    </v-btn>
  </v-container>
</template>

<style scoped>
.content-wrapper {
  max-height: 600px;
  overflow-y: auto;
}

.block-title {
  font-size: 16px;
  font-weight: 700;
  line-height: 24px; /* 150% */
}

.custom-checkbox {
  /* color: var(--Base-color-80, rgba(54, 57, 64, 0.8)); */
  color: var(--Base-color-100);
}

.show-all {
  text-transform: none;
  font-size: 16px;
  font-weight: 300;
  line-height: 24px; /* 150% */
  padding-left: 0;
  color: var(--Base-color-80, rgba(54, 57, 64, 0.8));
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: none;
  text-decoration-thickness: 7.5%; /* 1.2px */
  text-underline-offset: 15%; /* 2.4px */
  text-underline-position: from-font;
}

::v-deep(.v-list-item) {
  padding: 0 !important;
  margin-top: -4px !important;
}

::v-deep(.v-label) {
  margin-left: 8px;
  line-height: 1.3;
}

::v-deep(.v-input__details) {
  display: none;
}
</style>
