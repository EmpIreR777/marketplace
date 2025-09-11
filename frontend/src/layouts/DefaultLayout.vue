<script setup lang="ts">
import {provide, ref} from 'vue';
import {RouterView} from 'vue-router';
import NavigationDrawer from "@/components/common/NavigationDrawer.vue"
import DefaultHeader from '@/components/common/DefaultHeader.vue';
import DefaultFooter from '@/components/common/DefaultFooter.vue';
import FloatButton from "@/components/common/FloatButton.vue";
import DriverCombine from "@/components/common/DriverCombine.vue";
import AllFiltersBlock from "@/components/courses/coursesFilters/CoursesFilterMenu.vue";
import AccountMobileMenu from "@/components/account/AccountMobileMenu.vue";

const props = defineProps({
  showFooter: {
    type: Boolean,
    default: true,
  },
});


const drawer = ref(false);
const toggleDrawer = () => {
  drawer.value = !drawer.value;
};

const filterDrawer = ref(false);
const toggleFilterDrawer = () => {
  filterDrawer.value = !filterDrawer.value;
};

const accountMenuDrawer = ref(false);

const toggleAccountMenuDrawer = () => {
  accountMenuDrawer.value = !accountMenuDrawer.value;
}

provide('toggleFilterDrawer', toggleFilterDrawer);
</script>

<template>
  <v-app>
    <NavigationDrawer
      :drawer="drawer"
      @update:drawer="drawer = $event"
    />
    <DriverCombine
      :drawer="filterDrawer"
      @update:drawer="filterDrawer = $event"
    >
      <AllFiltersBlock/>
    </DriverCombine>
    <DriverCombine
      :drawer="accountMenuDrawer"
      @update:drawer="accountMenuDrawer = $event"
      :isDecorative="true"
    >
      <AccountMobileMenu @update:drawer="accountMenuDrawer = $event" />
    </DriverCombine>
    <DefaultHeader :toggle-drawer="toggleDrawer" :toggleAccountDrawer="toggleAccountMenuDrawer"/>
    <v-main>
      <v-container fluid class="main-section">
        <RouterView/>
      </v-container>
    </v-main>
    <DefaultFooter v-if="props.showFooter"/>
    <FloatButton/>
  </v-app>
</template>

<style scoped>
main {
  flex-grow: 1; /* Ensures main content grows to take available space */
  padding: 96px 0 0;

  @media (max-width: 870px) {
    padding: 64px 0 0;
  }
}

.main-section {
  padding: 0;
}
</style>


