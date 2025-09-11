<script setup lang="ts">
import AccountSidebar from '@/components/account/AccountSidebar.vue'
</script>

<template>
  <div class="account">
    <v-row>
      <!-- Боковое меню -->
      <v-col cols="0" md="3" class="d-none d-md-block">
        <AccountSidebar />
      </v-col>
      <!-- Контент -->
      <v-col cols="12" md="9" class="pb-md-8 pb-12">
        <router-view></router-view>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped></style>
