<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AllFiltersBlock from '@/components/courses/coursesFilters/CoursesFilterMenu.vue'

// Пропсы
const props = defineProps({
  drawer: { type: Boolean, required: true },
})

// Эмиттер для передачи событий родителю
const emit = defineEmits(['update:drawer'])

// Двустороннее связывание состояния
const localDrawer = computed({
  get: () => props.drawer,
  set: (value) => emit('update:drawer', value),
})

// Ширина экрана
const screenWidth = ref(window.innerWidth)

// Слушатель изменений размера окна
const updateScreenWidth = () => {
  screenWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', updateScreenWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenWidth)
})
</script>

<template>
  <v-navigation-drawer
    v-model="localDrawer"
    :location="$vuetify.display.mobile ? 'left' : undefined"
    temporary
    app
    :width="screenWidth"
    touchless
    class="custom-drawer py-12 px-4"
  >
    <div class="drawer-header">
      <v-btn height="24" icon variant="plain" @click="localDrawer = false">
        <v-icon size="24">mdi-close</v-icon>
      </v-btn>
    </div>
    <v-container
      class="d-flex flex-column align-start justify-start h-100 position-relative pa-0"
      fluid
    >
      <AllFiltersBlock />
    </v-container>
  </v-navigation-drawer>
</template>

<style>
.custom-drawer {
  height: 100vh;
}

.drawer-header {
  position: absolute;
  width: 100%;
  height: 40px;
  top: 0;
  left: 0;
  padding: 8px 12px;
}

.menu-item .v-list-item-title {
  font-size: 32px;
  font-style: normal;
  font-weight: 700;
  line-height: 48px; /* 150% */
}

.menu-nested-item {
  height: 20px !important;
  min-height: 20px !important;
  padding-left: 0 !important;
}

.menu-nested-item .v-list-item-title {
  font-size: 14px !important;
  font-style: normal;
  font-weight: 700;
  line-height: 20px; /* 142.857% */
}
</style>
