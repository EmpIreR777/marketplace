<script setup lang="ts">
import { AppColors } from '@/enums/appColors.ts'
// import FilterTrigger from '@/components/common/FilterTrigger.vue'
import NotificationMsg from '@/components/account/NotificationMsg.vue'
import { useNotificationsStore } from '@/stores/Account/notifications/index'
import { onUnmounted } from 'vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useDisplay } from 'vuetify'

const notificationsStore = useNotificationsStore()
const { xs, sm } = useDisplay()

function readNnotify(id: number) {
  notificationsStore.readNotification(id)
}

onUnmounted(() => {
  notificationsStore.clearStore()
})
</script>

<template>
  <div class="text-h5 font-weight-bold d-block d-md-none mb-2">Уведомления</div>
  <v-card :loading="notificationsStore.isLoading" elevation="0" class="pa-0">
    <v-card-title
      class="d-flex align-start flex-wrap flex-lg-nowrap justify-space-between pa-0 ga-4 align-center"
      style="white-space: wrap"
    >
      <div
        class="text-h5 font-weight-bold flex-fill text-count"
        :style="{ color: AppColors.MAIN_TEXT }"
      >
        {{ notificationsStore.notifyCount > 0 ? notificationsStore.notifyCount : 'нет' }}
        новых уведомлений
      </div>

      <div class="d-flex ga-4 align-center ml-auto">
        <BaseButton
          v-if="xs || sm"
          type="icon"
          icon="readAll"
          @click="notificationsStore.readAllNotifys"
        />
        <v-btn
          v-else
          variant="text"
          text="Отметить все как прочитанные"
          size="small"
          :color="AppColors.SECOND_TEXT"
          class="text-body-1 font-weight-light text-decoration-underline px-0"
          @click="notificationsStore.readAllNotifys"
        />
        <!-- <FilterTrigger :filter-visibility="false" @update-visibility="() => {}" /> -->
      </div>
    </v-card-title>

    <v-card-text class="pa-0">
      <v-infinite-scroll
        :key="notificationsStore.renderKey"
        :items="notificationsStore.infinteLoaderData"
        :onLoad="notificationsStore.loadOnScroll"
        class="w-100 ga-2"
        style="display: grid; grid-template-columns: 100%"
      >
        <NotificationMsg
          v-for="(notification, ndx) in notificationsStore.infinteLoaderData"
          :key="ndx"
          :notification
          @updateIsRead="readNnotify(notification.id)"
        />
        <template #empty></template>
      </v-infinite-scroll>
    </v-card-text>
  </v-card>
</template>

<style lang="scss" scoped>
.text-count {
  @include xs() {
    font-size: 16px !important;
    font-weight: 300 !important;
  }
}
</style>
