<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAccountStore } from "@/stores/Account";


const emit = defineEmits(["update:drawer"]);
const accountStore = useAccountStore();
const router = useRouter();


const handleItemClick = (value: string) => {
  accountStore.setAccountTab(value);
  emit("update:drawer", false); // Закрываем Drawer принудительно
  router.push("/account");
};
</script>

<template>
  <v-list class="align-self-center">
    <template v-for="(item, index) in accountStore.getMenuItems" :key="index">
      <v-list-item
          :title="item.title"
          :value="item.value"
          :active="accountStore.getAccountTab === item.value"
          class="menu-item py-5 pl-8"
          @click="handleItemClick(item.value)"
          active-class="custom-active-list-item"
      ></v-list-item>
    </template>
  </v-list>
</template>

<style scoped>
.menu-item .v-list-item-title {
  font-size: 32px;
  font-style: normal;
  font-weight: 700;
  line-height: 48px; /* 150% */
}

.custom-active-list-item {
  color: var(--Base-color-20, rgba(54, 57, 64, 0.20));
}
</style>
