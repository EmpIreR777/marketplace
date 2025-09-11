<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'
import { useUniversitiesStore } from '@/stores/Universities'
import BaseTextField from '@/components/common/BaseTextField.vue'
import SortingBar from '@/components/filters/SortingBar.vue'
import FilterTrigger from '@/components/filters/FilterTrigger.vue'
import FiltersPanel from '@/components/filters/FiltersPanel.vue'
import UniversityCard from '@/components/common/cards/UniversityCard.vue'
import type { Recordable } from '@/types'
import UniversitiesFilter from '@/components/filters/universities/UniversitiesFilter.vue'

const universitiesStore = useUniversitiesStore()
const router = useRouter()
const { xs, width } = useDisplay()
const isMobile = computed(() => width.value < 767)
const filterListRef = ref()

const handleVisibilityUpdate = (val: boolean) => {
  universitiesStore.setFilterVisibility(val)
  if (isMobile.value) {
    if (val) {
      document.body.classList.add('fixed-scroll')
    } else {
      document.body.classList.remove('fixed-scroll')
    }
  }
}

const handleSearchInput = async (val: string) => {
  universitiesStore.setSearch(val)
  await universitiesStore.loadUnversitiesFilters()
}

const handleSortingUpdate = (val: string | null) => {
  universitiesStore.setOrdering(val)
}

const handleFiltersUpdate = async (val: Recordable) => {
  universitiesStore.setFilters(val)
  await universitiesStore.loadUnversitiesFilters()
}

const handleFiltersReset = async () => {
  universitiesStore.resetFilters()
  await universitiesStore.loadUnversitiesFilters()
  // Clear filter inputs
  if (filterListRef.value) {
    filterListRef.value.checkListRef.forEach((checkList: any) => (checkList.search = ''))
    filterListRef.value.rangeListRef.forEach((rangeList: any) => rangeList.setRangeValues())
  }
}

function goToUniversityDetail(id: number) {
  router.push({ name: 'university-detail', params: { id, tab: 'programs' } })
}

onMounted(() => {
  universitiesStore.loadStore()
})

onUnmounted(() => {
  universitiesStore.clearStore()
})
</script>

<template>
  <div class="universities">
    <h2 class="universities__header-title">ВУЗы</h2>

    <div class="universities__header-filters">
      <BaseTextField
        v-if="!xs"
        v-model="universitiesStore.search"
        label="Поиск"
        prepend-inner-icon="mdi-magnify"
        :debounce="300"
        clearable
        class="universities__header-search"
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
          :ordering="universitiesStore.ordering"
          @update-sorting="handleSortingUpdate"
        />
        <FilterTrigger
          :filter-visibility="universitiesStore.isFiltersVisible"
          :is-reversed="xs"
          text="Фильтр"
          :count="universitiesStore.getActiveFiltersCount"
          @update-visibility="handleVisibilityUpdate"
        />
      </div>
    </div>

    <div class="universities__main">
      <v-infinite-scroll
        :key="universitiesStore.renderKey"
        :items="universitiesStore.infinteLoaderData"
        :onLoad="universitiesStore.loadOnScroll"
        class="d-flex flex-column w-100 overflow-hidden"
      >
        <UniversityCard
          v-for="(item, idx) in universitiesStore.infinteLoaderData"
          :key="item.id"
          :university="item"
          :hide-programs-count="universitiesStore.isFiltersVisible"
          :class="{ 'universities__card-border': !!idx }"
          @click="goToUniversityDetail(item.id)"
        />
        <template #empty></template>
      </v-infinite-scroll>

      <Teleport to="header" :disabled="!isMobile">
        <FiltersPanel
          v-if="universitiesStore.isFiltersVisible"
          :is-mobile="isMobile"
          style="min-width: 300px"
          @update-visibility="handleVisibilityUpdate"
          @reset="handleFiltersReset"
        >
          <UniversitiesFilter
            v-if="universitiesStore.getFiltersCatalog"
            ref="filterListRef"
            :filter-catalog="universitiesStore.getFiltersCatalog"
            :filters="universitiesStore.filters"
            :filters-update="handleFiltersUpdate"
          />
        </FiltersPanel>
      </Teleport>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.universities {
  display: flex;
  flex-direction: column;
  gap: 16px;

  &__org-raw {
    padding-bottom: 0;
    cursor: pointer;
  }

  &__header {
    &-title {
      @include typography('h3');

      @include xs {
        flex: 1;
        @include typography('h6');
      }
    }

    &-filters {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 32px;

      @include xs() {
        flex-direction: column;
        gap: 16px;
      }

      &-sort {
        display: flex;
        align-items: center;
        gap: 8px;
      }

      & > button {
        padding: 0;
      }
    }

    &-search {
      max-width: 300px;

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

    & .filter-container {
      min-width: calc(33.33% - (32px / 1.5)) !important;
      max-width: calc(33.33% - (32px / 1.5)) !important;

      @include md {
        min-width: calc(50% - (16px / 2)) !important;
        max-width: calc(50% - (16px / 2)) !important;
      }
    }
  }

  &__card-border {
    border-top: 1px solid $base-20;
  }
}
</style>
