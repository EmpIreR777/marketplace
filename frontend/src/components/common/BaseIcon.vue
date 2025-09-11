<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'

const iconList = import.meta.glob('../../assets/icons/*.vue')

const props = defineProps<{
  name: string
  fill?: string
  stroke?: string
  size?: string
  color?: string
}>()

const dynamicSvgIcon = computed(() => {
  const currentSvgIconsList = getIconList()
  if (props.name && currentSvgIconsList.includes(props.name))
    return defineAsyncComponent(() =>
      import(`../../assets/icons/${props.name}.vue`).catch((e) => console.warn(e)),
    )

  return ''
})

function getIconList() {
  return Object.keys(iconList).map((i) => {
    return i.split('/').reverse()[0].split('.')[0]
  })
}
</script>

<template>
  <v-icon :size="props.size || '24px'">
    <component :is="dynamicSvgIcon" :fill="props.fill || 'none'" :stroke="props.stroke || 'none'" />
  </v-icon>
</template>

<style lang="scss" scoped>
.pointer {
  cursor: pointer;
}
</style>
