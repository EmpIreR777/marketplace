<script setup lang="ts">
import { computed, provide, ref } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import NavigationDrawer from '@/components/common/NavigationDrawer.vue'
import DefaultHeader from '@/components/common/DefaultHeader.vue'
import DefaultFooter from '@/components/common/DefaultFooter.vue'
import FloatButton from '@/components/common/FloatButton.vue'
import DriverCombine from '@/components/common/DriverCombine.vue'
import AllFiltersBlock from '@/components/courses/coursesFilters/CoursesFilterMenu.vue'
import AccountMobileMenu from '@/components/account/AccountMobileMenu.vue'
import { useDisplay } from 'vuetify'

const props = defineProps({
  showFooter: {
    type: Boolean,
    default: true,
  },
})

const route = useRoute()
const { xs } = useDisplay()

const drawer = ref(false)
const toggleDrawer = () => {
  drawer.value = !drawer.value
}

const filterDrawer = ref(false)
const toggleFilterDrawer = () => {
  filterDrawer.value = !filterDrawer.value
}

const accountMenuDrawer = ref(false)

const toggleAccountMenuDrawer = () => {
  accountMenuDrawer.value = !accountMenuDrawer.value
}

provide('toggleFilterDrawer', toggleFilterDrawer)

const containerPaddingTop = computed(() =>
  route.path === '/' ? '16px' : xs.value ? '24px' : '32px',
)
</script>

<template>
  <NavigationDrawer :drawer="drawer" @update:drawer="drawer = $event" />
  <DriverCombine :drawer="filterDrawer" @update:drawer="filterDrawer = $event">
    <AllFiltersBlock />
  </DriverCombine>
  <DriverCombine
    :drawer="accountMenuDrawer"
    @update:drawer="accountMenuDrawer = $event"
    :isDecorative="true"
  >
    <AccountMobileMenu @update:drawer="accountMenuDrawer = $event" />
  </DriverCombine>

  <DefaultHeader :toggle-drawer="toggleDrawer" :toggleAccountDrawer="toggleAccountMenuDrawer" />

  <v-main>
    <v-container :style="{ paddingTop: containerPaddingTop }">
      <RouterView />
    </v-container>
  </v-main>

  <DefaultFooter v-if="props.showFooter" />
  <FloatButton />
</template>
