<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useDisplay } from 'vuetify'
import { AppColors } from '@/enums/appColors.ts'
import BaseButton from '@/components/common/BaseButton.vue'
import { useUser } from '@/stores/User'
import { useMyCoursesStore } from '@/stores/Account/my-courses'
import CourseCard from '@/components/common/CourseCard.vue'
import { VerificationStatus } from '@/enums/verificationStatuses'
import FilterTrigger from '@/components/filters/FilterTrigger.vue'
import CoursesFilters from '@/components/courses/CoursesFilters.vue'
import FiltersPanel from '@/components/filters/FiltersPanel.vue'
import type { Recordable } from '@/types'
import BaseTextField from '@/components/common/BaseTextField.vue'
import SortingBar from '@/components/filters/SortingBar.vue'
import { ORDERING_OPTIONS } from '@/enums/coursesFiltersEnum'

const userStore = useUser()
const myCoursesStore = useMyCoursesStore()
const { xs, sm } = useDisplay()
const isMobile = computed(() => xs.value || sm.value)
const filterListRef = ref()

interface Tab {
  title: string
  value: string
}

const tabs: Tab[] = [
  { title: 'UI/UX Дизайнер (Pro)', value: '1' },
  { title: 'second', value: '2' },
  { title: 'third', value: '3' },
]

const selectedTab = ref<string>('Мои курсы') // По умолчанию "О курсе"

const handleSortingUpdate = (val: string | null) => {
  myCoursesStore.setOrdering(val)
}

const handleVisibilityUpdate = (val: boolean) => {
  myCoursesStore.setFilterVisibility(val)
  if (isMobile.value) {
    if (val) {
      document.body.classList.add('fixed-scroll')
    } else {
      document.body.classList.remove('fixed-scroll')
    }
  }
}

const handleSearchInput = async (val: string) => {
  myCoursesStore.setSearch(val)
  await myCoursesStore.loadMyCoursesFilters()
}

const handleFiltersUpdate = async (val: Recordable) => {
  myCoursesStore.setFilters(val)
  await myCoursesStore.loadMyCoursesFilters()
}

const handleFiltersReset = async () => {
  myCoursesStore.resetFilters()
  await myCoursesStore.loadMyCoursesFilters()
  // Clear filter inputs
  if (filterListRef.value) {
    filterListRef.value.checkListRef.forEach((checkList: any) => (checkList.search = ''))
    filterListRef.value.rangeListRef.forEach((rangeList: any) => rangeList.setRangeValues())
  }
}

onMounted(() => {
  myCoursesStore.loadStore()
})

onUnmounted(() => {
  myCoursesStore.clearStore()
})
</script>

<template>
  <v-card
    elevation="0"
    :loading="myCoursesStore.isLoading"
    class="my-courses"
    :class="{ filter: myCoursesStore.isFiltersVisible }"
  >
    <v-card-title
      class="d-flex align-center flex-nowrap justify-space-between pa-0 ga-4"
      style="white-space: wrap"
    >
      <div
        class="text-h5 font-weight-bold flex-fill text-no-wrap"
        :style="{ color: AppColors.MAIN_TEXT }"
      >
        Мои курсы
      </div>
      <div class="d-flex w-sm-auto ga-4 ml-auto">
        <v-select
          v-if="false"
          class="w-100 w-sm-auto"
          :min-width="230"
          v-model="selectedTab"
          :items="tabs"
          item-title="title"
          item-value="value"
          variant="outlined"
          rounded="lg"
          hide-details
        />

        <BaseButton
          to="/course-editor"
          label="Новый курс"
          :disabled="userStore.getVerifiedStatus !== VerificationStatus.VERIFIED"
          class="my-courses__header-add-course"
        />
      </div>
    </v-card-title>

    <v-card-subtitle
      v-if="userStore.getVerifiedStatus !== VerificationStatus.VERIFIED"
      class="py-0"
    >
      <div class="mdb text-center">Для создания курса пройдите верификацию !</div>
    </v-card-subtitle>

    <div class="my-courses__header-filters">
      <BaseTextField
        v-model="myCoursesStore.search"
        label="Поиск"
        prepend-inner-icon="mdi-magnify"
        :debounce="300"
        clearable
        class="my-courses__header-search"
        @update:modelValue="handleSearchInput"
      />
      <div
        class="d-flex w-100 w-sm-auto align-center justify-space-between justify-sm-end pa-2 border-mobile ga-4"
      >
        <SortingBar
          :items="ORDERING_OPTIONS"
          :is-reversed="xs"
          class="order-1 order-sm-0"
          :ordering="myCoursesStore.ordering"
          @update-sorting="handleSortingUpdate"
        />
        <FilterTrigger
          :filter-visibility="myCoursesStore.isFiltersVisible"
          :is-reversed="xs"
          text="Фильтр"
          :count="myCoursesStore.getActiveFiltersCount"
          @update-visibility="handleVisibilityUpdate"
        />
      </div>
    </div>

    <div class="my-courses__main">
      <v-infinite-scroll
        :key="myCoursesStore.renderKey"
        :items="myCoursesStore.infinteLoaderData"
        :onLoad="myCoursesStore.loadOnScroll"
      >
        <div class="my-courses__grid">
          <CourseCard
            v-for="course in myCoursesStore.infinteLoaderData"
            :key="course.id"
            :course="course"
            :isEditable="userStore.isAuthor"
            class="my-courses__card"
          />
        </div>
        <template v-slot:loading>
          <div class="my-courses__loader-container">
            <v-progress-circular indeterminate />
          </div>
        </template>
        <template v-slot:empty></template>
      </v-infinite-scroll>

      <Teleport to="header" :disabled="!isMobile">
        <FiltersPanel
          v-if="myCoursesStore.isFiltersVisible"
          :is-mobile="isMobile"
          @reset="handleFiltersReset"
          @update-visibility="handleVisibilityUpdate"
        >
          <CoursesFilters
            v-if="myCoursesStore.getFiltersCatalog"
            ref="filterListRef"
            :filter-catalog="myCoursesStore.getFiltersCatalog"
            :filters="myCoursesStore.filters"
            :filters-update="handleFiltersUpdate"
          />
        </FiltersPanel>
      </Teleport>
    </div>
  </v-card>
</template>

<style lang="scss" scoped>
.my-courses {
  display: flex;
  flex-direction: column;
  gap: 16px;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;

    @include sm() {
      flex-wrap: wrap;
    }

    &-title {
      @include typography('h6');
      @include xs() {
        margin-bottom: 8px;
      }
    }

    &-add-course {
      padding: 16px 32px;

      @include xs() {
        padding: 8px 16px;
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

  &__loader-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 12px;
  }

  & .v-infinite-scroll {
    overflow: hidden;
    width: 100%;
  }

  &.filter .v-infinite-scroll {
    width: calc(66.66% - (32px / 3));

    @include md {
      width: calc(50% - (16px / 3));
    }
    @include sm {
      width: calc(50% - 16px);
    }
  }

  & .v-infinite-scroll__side {
    padding: 0;
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
      width: calc(33.33% - (32px / 1.5));

      @include md {
        width: calc(50% - (16px / 2));
      }
    }
  }

  &__grid {
    width: 100%;
    gap: 32px;
    display: flex;
    flex-wrap: wrap;

    @include md {
      gap: 16px;
    }

    & .my-courses__card {
      height: fit-content !important;
      width: calc(33.33% - (32px / 1.5));
      @include md {
        width: calc(50% - (16px / 2));
      }
      @include xs {
        width: 100%;
      }
    }
  }

  &.filter {
    & .my-courses__card {
      width: calc(50% - (32px / 2));
      @include md {
        width: 100%;
      }
    }
    @include xs {
      grid-template-columns: 1fr;
    }
  }

  &__filter {
    position: relative;
    transition: $transition;
    overflow: hidden;
    opacity: 0;
    width: 0;

    &.fade {
      opacity: 1;
      width: auto;
    }
  }
}
.border-mobile {
  @include xs {
    border-radius: 8px;
    border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
  }
}
</style>
