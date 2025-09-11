<script setup lang="ts">
import { computed, ref } from 'vue'
import { useDisplay } from 'vuetify'
import SliderCategory from '@/components/sliders/SliderCategory.vue'
import BaseTextField from '@/components/common/BaseTextField.vue'
import { CoursesCategoryEnum } from '@/enums/coursesFiltersEnum'

const props = defineProps<{
  title: string
  counters: Record<CoursesCategoryEnum, number>
  searchInput: string
}>()

const emits = defineEmits<{
  (e: 'update-search', queryString: string): void
  (e: 'update-filters', val: CoursesCategoryEnum): void
}>()

const { xs } = useDisplay()
const search = ref<string>(props.searchInput)
const openMobileSearch = ref<boolean>(false)

const showMobileSearch = computed(() => xs.value && openMobileSearch.value)

function handleOpenMobileSearch() {
  openMobileSearch.value = !openMobileSearch.value
}
</script>

<template>
  <v-row class="mx-0">
    <h2 class="courses-header__title">{{ title }}</h2>
    <v-btn
      variant="text"
      size="32"
      class="direction-sort-button d-sm-none align-self-center"
      @click="handleOpenMobileSearch"
    >
      <v-icon :icon="openMobileSearch ? 'mdi-close' : 'mdi-magnify'" size="24" />
    </v-btn>
  </v-row>
  <BaseTextField
    v-if="showMobileSearch"
    v-model="search"
    label="Поиск"
    prepend-inner-icon="mdi-magnify"
    :debounce="300"
    class="courses__header-search"
    @update:modelValue="emits('update-search', $event)"
  />
  <SliderCategory
    :counters="props.counters"
    class="courses-header__slider"
    @update-filters="emits('update-filters', $event)"
  />
</template>

<style scoped lang="scss">
.courses-header {
  &__title {
    @include typography('h3');

    @include xs {
      flex: 1;
      @include typography('h6');
    }
  }

  &__slider {
    margin-top: 36px;

    @include xs {
      margin-top: 1rem;
    }
  }
}

::v-deep(.v-input__details) {
  display: none;
}

::v-deep(.v-field) {
  border-radius: 12px;
}
</style>
