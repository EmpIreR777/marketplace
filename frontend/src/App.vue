<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import BaseSnackbar from '@/components/common/BaseSnackbar.vue'
import { useMetrika } from '@/composable/useMetrika'

const { jivoDialogStart } = useMetrika()

onMounted(() => {
  const jivo = import.meta.env.VITE_JIVO_KEY
  if (jivo) {
    const script = document.createElement('script')
    script.src = `//code.jivo.ru/widget/${import.meta.env.VITE_JIVO_KEY}`
    script.async = true
    document.body.appendChild(script)
  }

  window.jivo_onClientStartChat = function () {
    jivoDialogStart()
  }
})
</script>

<template>
  <v-app>
    <RouterView />
    <BaseSnackbar />
  </v-app>
</template>
