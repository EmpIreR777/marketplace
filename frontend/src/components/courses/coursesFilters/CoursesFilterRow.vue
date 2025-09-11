<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { useRoute, useRouter } from 'vue-router'
import { useCoursesFilterStore } from '@/stores/CoursesFilter'
import { priceIcon, filterIcon } from '@/assets/icons'
import {
  SORTING_FIELDS_TRANSLATE,
  SortingDirectionEnum,
  SORTING_API_FIELDS,
} from '@/enums/coursesFiltersEnum'
import type { SelectedFilters } from '@/stores/CoursesFilter/modele'
import { useCoursesStore } from '@/stores/Courses'
import BaseButton from '@/components/common/BaseButton.vue'
import { useMetrika } from '@/composable/useMetrika.ts'

const route = useRoute()
const router = useRouter()
const coursesFilterStore = useCoursesFilterStore()
const { changeCourseFilter } = useMetrika()
const coursesStore = useCoursesStore()

const selectedSort = ref(SORTING_FIELDS_TRANSLATE.PRICE as string)
const isDescending = ref(false)

const emit = defineEmits(['toggleFilterMenu'])

const setSortOption = (sortOption: string) => {
  selectedSort.value = sortOption
}

const toggleSortingDirection = () => {
  isDescending.value = !isDescending.value
}

const toggleFilter = (event: MouseEvent) => {
  event.stopPropagation()
  emit('toggleFilterMenu')
}

function handleSearchInput(queryString: string) {
  coursesFilterStore.setSelectedFilters({ name: queryString })
}

const updateFilters = () => {
  router.push({
    path: route.path,
    query: { ...coursesFilterStore.getSelectedFilters }, // Add params to url
  })
  changeCourseFilter()
  coursesStore.clearCourses()
}

const emitUpdateDebounced = useDebounceFn(updateFilters, 300)

watch(
  [selectedSort, isDescending],
  ([newSort, newRotation]) => {
    if (newSort === SORTING_FIELDS_TRANSLATE.PRICE) {
      const sortingDirectionAttr = newRotation
        ? SortingDirectionEnum.ASC
        : SortingDirectionEnum.DESC
      coursesFilterStore.setSelectedFilters({
        ordering: `${sortingDirectionAttr}${SORTING_API_FIELDS.PRICE}`,
      })
    }
  },
  { flush: 'sync' },
)

watch(() => coursesFilterStore.getSelectedFilters, emitUpdateDebounced, { deep: true })

onMounted(() => {
  if (Object.keys(route.query).length > 0) {
    coursesFilterStore.setSelectedFilters({ ...(route.query as SelectedFilters) }) // Set query params to filters
  }

  coursesFilterStore.loadCoursesFilters()
})
</script>
<template>
  <v-container
    class="d-none d-sm-flex menu-bar py-4 px-0 justify-space-between align-center mt-3 mt-md-8"
  >
    <!-- Поле поиска -->
    <v-text-field
      :model-value="coursesFilterStore.getSelectedFilters?.name"
      variant="outlined"
      placeholder="Поиск"
      prepend-inner-icon="mdi-magnify"
      class="search-field"
      rounded="lg"
      @update:modelValue="handleSearchInput"
    ></v-text-field>

    <!-- Сортировка и фильтры -->
    <div class="d-flex align-center">
      <!-- Сортировка -->
      <v-menu offset-y left>
        <template #activator="{ props }">
          <v-btn v-bind="props" variant="text" class="menu-sort-button">
            {{ selectedSort }}
            <!-- Display selected sort option -->
          </v-btn>
        </template>
        <v-list class="select-menu" :style="{ borderRadius: '12px' }">
          <!-- <v-list-item class="py-2" @click="setSortOption(SORTING_FIELDS_TRANSLATE.POPULARITY)">{{ SORTING_FIELDS_TRANSLATE.POPULARITY }}</v-list-item>
          <v-list-item class="py-2" @click="setSortOption(SORTING_FIELDS_TRANSLATE.RATING)">{{ SORTING_FIELDS_TRANSLATE.RATING }}</v-list-item> -->
          <v-list-item class="py-2" @click="setSortOption(SORTING_FIELDS_TRANSLATE.PRICE)">{{
            SORTING_FIELDS_TRANSLATE.PRICE
          }}</v-list-item>
        </v-list>
      </v-menu>

      <BaseButton
        icon="sort-ascending"
        type="icon"
        :rotate-icon="isDescending"
        @click="toggleSortingDirection"
      />

      <!-- Фильтр -->
      <v-btn variant="text" class="filter-button" @click="toggleFilter">
        фильтр
        <v-img class="ml-2" :src="filterIcon" width="24" height="24" cover></v-img>
      </v-btn>
    </div>
  </v-container>
  <v-container class="mx-0 mb-4 mt-4 pa-2 mobil-filter d-sm-none" justify="space-between">
    <div class="d-flex align-center ga-2 cursor-pointer w-auto" @click="toggleFilter">
      <v-img class="ml-2 flex-0-0" :src="filterIcon" width="16" height="16" cover></v-img>
      <div class="d-flex align-start flex-column">
        <span class="mdb">Фильтр</span>
        <span v-if="coursesFilterStore.getActiveFiltersCount > 0" class="sm">
          Выбрано {{ coursesFilterStore.getActiveFiltersCount }}
        </span>
        <span v-else class="sm">Не выбран</span>
      </div>
    </div>
    <div class="d-flex align-center cursor-pointer">
      <v-btn variant="text" class="direction-sort-button px-0" @click="toggleSortingDirection">
        <v-img
          :src="priceIcon"
          width="16"
          height="16"
          cover
          :class="{ rotated: isDescending }"
          class="direction-sort-button__img"
        ></v-img>
      </v-btn>
      <div class="direction-sort-text">
        <v-menu activator="parent" offset-y left>
          <template #activator="{ props }">
            <v-btn v-bind="props" variant="text" class="menu-sort-button-mobil" height="16">
              Сортировка
            </v-btn>
            <span class="menu-sort-title">{{ selectedSort }}</span>
          </template>
          <v-list class="select-menu-mobil" :style="{ borderRadius: '12px' }">
            <!-- <v-list-item class="py-2" @click="setSortOption(SORTING_FIELDS_TRANSLATE.POPULARITY)">{{ SORTING_FIELDS_TRANSLATE.POPULARITY }}</v-list-item>
            <v-list-item class="py-2" @click="setSortOption(SORTING_FIELDS_TRANSLATE.RATING)">{{ SORTING_FIELDS_TRANSLATE.RATING }}</v-list-item> -->
            <v-list-item class="py-2" @click="setSortOption(SORTING_FIELDS_TRANSLATE.PRICE)">{{
              SORTING_FIELDS_TRANSLATE.PRICE
            }}</v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>
  </v-container>
</template>

<style scoped>
.search-field {
  width: 300px;
  flex-grow: 0;
}
::v-deep(.v-input__details) {
  display: none;
}
.select-menu {
  width: 240px;
  transform: translateX(-81px);
  border-radius: 12px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
  background: var(--White-color-100, #fff);
}

.select-menu-mobil {
  width: 240px;
  transform: translate(8px, 12px);
  border-radius: 12px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
  background: var(--White-color-100, #fff);
}
.menu-sort-button {
  text-transform: none;
  font-weight: 400;
  width: auto;
  justify-content: end;
}

.menu-sort-button-mobil {
  text-transform: none;
  width: auto;
  max-width: 110px;
  justify-content: start;
  flex-wrap: wrap;
  padding: 0;
  font-size: 14px;
  font-style: normal;
  font-weight: 700;
  line-height: 20px;
}

.menu-sort-title {
  margin-top: 4px;
  font-size: 12px;
  font-style: normal;
  font-weight: 300;
  line-height: 16px;
}

.direction-sort-text {
  display: flex;
  flex-direction: column;
  align-content: start;
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

.filter-button {
  text-transform: none;
  font-weight: 400;
}

.mobil-filter {
  display: flex;
  justify-content: space-between;
  border-radius: 8px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
  background: var(--White-color-100, #fff);
}
</style>
