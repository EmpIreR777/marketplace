<script setup lang="ts">
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import BaseTextField from '@/components/common/BaseTextField.vue'
import SortingBar from '@/components/filters/SortingBar.vue'
import FilterTrigger from '@/components/filters/FilterTrigger.vue'
import { useUniversityDetailStore } from '@/stores/UniversityDetail'
import ProgramCard from '@/components/common/cards/ProgramCard.vue'
import type { Recordable } from '@/types'
import FiltersPanel from '@/components/filters/FiltersPanel.vue'
import CoursesFilters from '@/components/courses/CoursesFilters.vue'

const universityDetailStore = useUniversityDetailStore()
const { xs, width } = useDisplay()
const isMobile = computed(() => width.value < 767)

const handleSearchInput = async (val: string) => {
  universityDetailStore.setSearch(val)
  await universityDetailStore.loadProgramsFilters()
}

const handleSortingUpdate = (val: string | null) => {
  universityDetailStore.setOrdering(val)
}

const handleVisibilityUpdate = (val: boolean) => {
  universityDetailStore.setFilterVisibility(val)
  if (isMobile.value) {
    if (val) {
      document.body.classList.add('fixed-scroll')
    } else {
      document.body.classList.remove('fixed-scroll')
    }
  }
}

const handleFiltersReset = async () => {
  universityDetailStore.resetFilters()
  await universityDetailStore.loadProgramsFilters()
}

const handleFiltersUpdate = async (val: Recordable) => {
  universityDetailStore.setFilters(val)
  await universityDetailStore.loadProgramsFilters()
}
</script>

<template>
  <div class="programs" :class="{ filter: universityDetailStore.isFiltersVisible }">
    <!-- Filter -->
    <div class="programs__filter">
      <BaseTextField
        v-model="universityDetailStore.search"
        label="Поиск"
        :prepend-inner-icon="xs ? '' : 'mdi-magnify'"
        :debounce="300"
        class="programs__filter-search"
        @update:modelValue="handleSearchInput"
      />

      <div
        class="d-flex w-100 w-sm-auto align-center justify-space-between justify-sm-end pa-2 border-mobile ga-4"
      >
        <SortingBar
          :items="[
            { apiKey: 'name', label: 'Название' },
            { apiKey: 'price', label: 'Цена' },
          ]"
          :is-reversed="xs"
          class="order-1 order-sm-0"
          :ordering="universityDetailStore.ordering"
          @update-sorting="handleSortingUpdate"
        />
        <FilterTrigger
          :filter-visibility="universityDetailStore.isFiltersVisible"
          :is-reversed="xs"
          text="Фильтр"
          :count="universityDetailStore.getActiveFiltersCount"
          @update-visibility="handleVisibilityUpdate"
        />
      </div>
    </div>
    <!-- Programs -->
    <div class="programs__main">
      <v-infinite-scroll
        :key="universityDetailStore.renderKey"
        :items="universityDetailStore.infinteLoaderData"
        :onLoad="universityDetailStore.loadOnScroll"
        class="programs__infinite-scroll"
      >
        <div class="programs__grid">
          <ProgramCard
            v-for="program in universityDetailStore.infinteLoaderData"
            :key="program.id"
            :program="program"
          />
        </div>
        <template v-slot:loading>
          <div class="programs__loader-container">
            <v-progress-circular indeterminate />
          </div>
        </template>
        <template v-slot:empty></template>
      </v-infinite-scroll>
      <Teleport to="header" :disabled="!isMobile">
        <FiltersPanel
          v-if="universityDetailStore.isFiltersVisible"
          :is-mobile="isMobile"
          @update-visibility="handleVisibilityUpdate"
          @reset="handleFiltersReset"
        >
          <CoursesFilters
            v-if="universityDetailStore.getFiltersCatalog"
            :filter-catalog="universityDetailStore.getFiltersCatalog"
            :filters="universityDetailStore.filters"
            :filters-update="handleFiltersUpdate"
          />
        </FiltersPanel>
      </Teleport>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.programs {
  display: flex;
  flex-direction: column;
  gap: 16px;

  &__filter {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 32px;

    @include xs() {
      flex-direction: column;
      gap: 8px;
    }

    &-sort {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    & > button {
      padding: 0;
    }

    &-search {
      max-width: 800px;

      @include xs() {
        max-width: 100%;
        width: 100%;
      }
    }
  }

  &__main {
    display: flex;
    justify-content: center;
    gap: 32px;
    width: 100%;

    @include md {
      gap: 16px;
    }
  }

  &__infinite-scroll {
    width: 100%;
    overflow: hidden;
  }

  &__grid {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
  }

  &__loader-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 12px;
  }
}
</style>
