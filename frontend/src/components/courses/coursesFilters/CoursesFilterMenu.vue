<script setup lang="ts">
import { computed } from 'vue'
// import { useRoute, useRouter } from 'vue-router';
import { useCoursesFilterStore } from '@/stores/CoursesFilter'
import { FILTER_PROPERTIES_NAMES } from '@/api/coursesFilters/constants'
import { FILTER_PROPERTIES_TITLES } from '@/enums/coursesFiltersEnum'
import CheckBoxListFilter from './filters/CheckBoxListFilter.vue'
// import RatingFilter from "./filters/RatingFilter.vue";
// import LocationFilter from "./filters/LocationFilter.vue";
import RangeFilter from './filters/RangeFilter.vue'

defineProps<{
  isPriceHidden?: boolean
}>()

const coursesThematicsCountShow = 5

// const route = useRoute();
// const router = useRouter();

const coursesFilterStore = useCoursesFilterStore()
// const resetFlag = ref(false);

const getPriceValue = (key: string, defaultValue = 0) => {
  return (
    coursesFilterStore.getSelectedFilters?.[key]?.toString() ?? null
    // coursesFilterStore.getCoursesFilters?.price?.[key]?.toString() ??
    // defaultValue.toString()
  )
}

const minPrice = computed(() => getPriceValue(FILTER_PROPERTIES_NAMES.price_min))
const maxPrice = computed(() => getPriceValue(FILTER_PROPERTIES_NAMES.price_max))

const resetFilterSelections = () => {
  coursesFilterStore.clearSelectedCheckboxFilters()
  coursesFilterStore.setSelectedFilters({
    [FILTER_PROPERTIES_NAMES.price_min]: '',
  })
  coursesFilterStore.setSelectedFilters({
    [FILTER_PROPERTIES_NAMES.price_max]: '',
  })

  // if (route.query.selectedCourses) {
  //   const restQueryParams = { ...route.query };
  //   delete restQueryParams.selectedCourses;
  //   router.replace({ path: route.path, query: restQueryParams });
  // }
}

const handlePriceRangeFilter = (data: { selectedValues: string[]; title: string }) => {
  // console.log(data.title, data.selectedValues);
  if (
    parseFloat(coursesFilterStore.getSelectedFilters?.price_min as string) ===
      parseFloat(data.selectedValues[0]) &&
    parseFloat(data.selectedValues[1]) < parseFloat(data.selectedValues[0])
  ) {
    return
  }
  coursesFilterStore.setSelectedFilters({
    [FILTER_PROPERTIES_NAMES.price_min]: data.selectedValues[0],
  })

  if (parseFloat(data.selectedValues[1]) > parseFloat(data.selectedValues[0])) {
    coursesFilterStore.setSelectedFilters({
      [FILTER_PROPERTIES_NAMES.price_max]: data.selectedValues[1],
    })
  } else {
    coursesFilterStore.setSelectedFilters({
      [FILTER_PROPERTIES_NAMES.price_max]: '',
    })
  }
}
</script>

<template>
  <div class="courses-filter-menu">
    <!-- <v-btn class="reset" variant="text" @click="resetFilterSelections">Сбросить</v-btn> -->
    <!--       @update:selected="handleCheckboxChange" -->
    <CheckBoxListFilter
      :data-checkbox="coursesFilterStore.getCoursesFilters?.learning_types || []"
      :title="FILTER_PROPERTIES_TITLES[FILTER_PROPERTIES_NAMES.learning_types]"
      :filterKey="FILTER_PROPERTIES_NAMES.learning_types"
      :key="FILTER_PROPERTIES_NAMES.learning_types"
      label="Поиск"
      :number-checkboxes="coursesThematicsCountShow"
    />
    <CheckBoxListFilter
      :data-checkbox="coursesFilterStore.getCoursesFilters?.courses_thematics || []"
      :title="FILTER_PROPERTIES_TITLES[FILTER_PROPERTIES_NAMES.courses_thematics]"
      :filterKey="FILTER_PROPERTIES_NAMES.courses_thematics"
      :key="FILTER_PROPERTIES_NAMES.courses_thematics"
      label="Поиск"
      :number-checkboxes="coursesThematicsCountShow"
    />
    <RangeFilter
      v-if="!isPriceHidden"
      :title="FILTER_PROPERTIES_TITLES[FILTER_PROPERTIES_NAMES.price]"
      :filterKey="FILTER_PROPERTIES_NAMES.price"
      :min="minPrice"
      :max="maxPrice"
      @update:selected="handlePriceRangeFilter"
    />

    <!-- :reset="resetFlag" -->
    <!-- <CheckBoxListFilter
      :data-checkbox="courseTrialVersion"
      title="Пробная версия"
      :number-checkboxes="coursesThematicsCountShow"
      @update:selected="handleCheckboxChange"
      :reset="resetFlag"
    /> -->
    <!-- <CheckBoxListFilter
      :data-checkbox="courseAgeCategory"
      title="Возрастная категория"
      :number-checkboxes="coursesThematicsCountShow"
      @update:selected="handleCheckboxChange"
      :reset="resetFlag"
    /> -->
    <!--       @update:selected="handleCheckboxChange" -->
    <!-- <CheckBoxListFilter
      :data-checkbox="coursesFilterStore.getCoursesFilters?.courses_thematics || []"
      :title="FILTER_PROPERTIES_TITLES[FILTER_PROPERTIES_NAMES.courses_thematics]"
      :filterKey="FILTER_PROPERTIES_NAMES.course_formats"
      :number-checkboxes="coursesThematicsCountShow"
    /> -->
    <CheckBoxListFilter
      :data-checkbox="coursesFilterStore.getCoursesFilters?.course_formats || []"
      :title="FILTER_PROPERTIES_TITLES[FILTER_PROPERTIES_NAMES.course_formats]"
      :filterKey="FILTER_PROPERTIES_NAMES.course_formats"
      :number-checkboxes="coursesThematicsCountShow"
    />
    <!-- <LocationFilter @update:selected="handleCheckboxChange" :reset="resetFlag" /> -->
    <!-- <CheckBoxListFilter
      :data-checkbox="courseTypeInstitution"
      title="Тип учебного заведения"
      :number-checkboxes="coursesThematicsCountShow"
      @update:selected="handleCheckboxChange"
      :reset="resetFlag"
    /> -->
    <!-- <CheckBoxListFilter
      :data-checkbox="courseCertificate"
      title="Документ об окончании"
      :number-checkboxes="coursesThematicsCountShow"
      @update:selected="handleCheckboxChange"
      :reset="resetFlag"
    /> -->
    <!-- <CheckBoxListFilter
      :data-checkbox="courseTypeEducational"
      title="Тип образовательной программы"
      :number-checkboxes="coursesThematicsCountShow"
      @update:selected="handleCheckboxChange"
      :reset="resetFlag"
    /> -->
    <!--       @update:selected="handleCheckboxChange" -->
    <CheckBoxListFilter
      :data-checkbox="coursesFilterStore.getCoursesFilters?.course_levels || []"
      :title="FILTER_PROPERTIES_TITLES[FILTER_PROPERTIES_NAMES.course_levels]"
      :filterKey="FILTER_PROPERTIES_NAMES.course_levels"
      :number-checkboxes="coursesThematicsCountShow"
    />
    <CheckBoxListFilter
      :data-checkbox="coursesFilterStore.getCoursesFilters?.is_state || []"
      :title="FILTER_PROPERTIES_TITLES[FILTER_PROPERTIES_NAMES.is_state]"
      :filterKey="FILTER_PROPERTIES_NAMES.is_state"
      :number-checkboxes="coursesThematicsCountShow"
    />
    <!-- <RatingFilter :reset="resetFlag" @update:selected="handleCheckboxChange" /> -->
  </div>
</template>

<style scoped lang="scss">
.courses-filter-menu {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.reset {
  position: absolute;
  right: 24px;
  top: 16px;
  text-transform: none;
  font-size: 16px;
  font-weight: 400;
  line-height: 24px; /* 150% */
  padding: 0;
  color: var(--Base-color-80, rgba(54, 57, 64, 0.8));
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: none;
  text-decoration-thickness: 7.5%; /* 1.2px */
  text-underline-offset: 15%; /* 2.4px */
  text-underline-position: from-font;
}
</style>
