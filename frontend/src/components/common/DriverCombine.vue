<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { deco1, deco2, deco3 } from '@/assets/navigation'

const props = defineProps({
  drawer: { type: Boolean, required: true },
  isDecorative: { type: Boolean, required: false },
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
    <v-img v-if="isDecorative" cover :src="deco1" class="menu-deco1"></v-img>

    <v-img v-if="isDecorative" cover :src="deco2" class="menu-deco2"></v-img>

    <v-img v-if="isDecorative" cover :src="deco3" class="menu-deco3"></v-img>
    <v-container
      class="d-flex flex-column align-start justify-center h-100 position-relative pa-0"
      fluid
    >
      <slot></slot>
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
  padding: 12px;
}

.menu-deco1 {
  position: absolute;
  top: 80px;
  left: 17px;
  width: 67px;
  height: 85px;
}

.menu-deco2 {
  position: absolute;
  top: 408px;
  right: 16px;
  width: 124px;
  height: 58px;
}

.menu-deco3 {
  position: absolute;
  bottom: 88px;
  left: 48px;
  width: 62px;
  height: 42px;
}

.menu-item .v-list-item-title {
  font-size: 32px;
  font-style: normal;
  font-weight: 700;
  line-height: 48px; /* 150% */
}

.menu-nested-item .v-list-item-title {
  font-size: 14px !important;
  font-style: normal;
  font-weight: 700;
  line-height: 20px; /* 142.857% */
}
</style>
