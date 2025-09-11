<script setup lang="ts">
import BaseIcon from "@/components/common/BaseIcon.vue";
</script>


<template>
  <template>
    <v-btn icon class="float-button">
      <BaseIcon name="help" />
      <!-- <v-img
        :src="helpIcon"
        max-width="24"
        max-height="24"
      ></v-img> -->
    </v-btn>
  </template>
</template>


<style scoped>
.float-button {
  position: fixed;
  right: 32px;
  top: 650px;
  z-index: 1000;
}
</style>
