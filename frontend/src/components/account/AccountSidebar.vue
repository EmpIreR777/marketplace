<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { AppColors } from '@/enums/appColors.ts'
import { useAccountStore } from '@/stores/Account'
import { useNotificationsStore } from '@/stores/Account/notifications'
import { ref } from 'vue'
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useUser } from '@/stores/User'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()
const userStore = useUser()
const notificationsStore = useNotificationsStore()

const logoutDialog = ref(false)

const onSelectNTabs = (tab: string) => {
  if (tab === 'logout') {
    logoutDialog.value = true
    return
  }

  router.push(`/account/${tab}`)
}
</script>

<template>
  <div class="account-sidebar">
    <v-list class="py-0 custom-list">
      <v-list-item
        v-for="item in accountStore.getMenuItems"
        :key="item.value"
        :prepend-icon="item.icon"
        :title="item.title"
        class="py-4 custom-list-item"
        active-class="custom-active-list-item"
        :active="route.name === item.value"
        @click="onSelectNTabs(item.value)"
      >
        <template
          v-slot:append
          v-if="item.value === 'notifications' && notificationsStore.notifyCount"
        >
          <v-badge
            :color="AppColors.BASE_COLOR_100"
            :text-color="AppColors.ACCENT_COLOR_LIME_100"
            :content="notificationsStore.notifyCount"
            class="custom-badge"
            inline
          />
        </template>
      </v-list-item>
    </v-list>

    <BaseDialog
      v-model="logoutDialog"
      title="Подтверждение"
      text="Вы действительно хотите выйти из учетной записи?"
      confirmText="Да"
      cancelText="Нет"
      @confirm="userStore.logoutUser()"
    />
  </div>
</template>

<style lang="scss">
.account-sidebar {
  .custom-list {
    border-radius: 16px !important;
    border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2)) !important;
  }

  .custom-list-item {
    font-size: 16px;
    font-style: normal;
    font-weight: 300;
    line-height: 24px;
  }

  :deep(.v-list-item__overlay) {
    background-color: var(--Accent-color-Lime-10, rgba(221, 255, 51, 0.1)) !important;
  }

  .custom-active-list-item {
    background: var(--Accent-color-Lime-10, rgba(221, 255, 51, 0.1)) !important;
  }

  & .v-card-actions {
    background: green;
  }
}
</style>
