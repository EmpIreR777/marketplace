<script setup lang="ts">
import { AppColors } from '@/enums/appColors.ts'
import type { INotification } from '@/api/notifications/models'
import { useDateFormat } from '@vueuse/core'

const props = defineProps<{
  notification: INotification
}>()

const emits = defineEmits<{
  (e: 'updateIsRead', val: boolean): void
}>()

function readNotify() {
  if (!props.notification.is_read) {
    emits('updateIsRead', true)
  }
}
</script>

<template>
  <div class="notification-msg" :class="{ read: !notification.is_read }" @mouseenter="readNotify">
    <div class="notification-msg__main">
      <div>
        <div class="notification-msg__title">
          {{ notification.title }}
        </div>
        <div class="notification-msg__date">
          {{ useDateFormat(notification.created_at, 'YYYY-MM-DD HH:mm') }}
        </div>
      </div>

      <div>
        <v-chip
          class="notification-msg__badge rounded-pill font-weight-light"
          :color="AppColors.ACCENT_BG"
          variant="flat"
          label
          size="large"
          density="compact"
        >
          {{ notification.notification_type }}
        </v-chip>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.notification-msg {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px 24px !important;
  border: 1px solid $base-20;
  border-radius: 16px;
  &.read {
    background-color: $lime-10;
    border-color: $lime-10;
  }

  &__main {
    display: flex;
    justify-content: space-between;
    @include xs() {
      flex-direction: column;
    }
  }

  &__title {
    @include typography('lg');
    color: $base;
  }

  &__date {
    @include typography('sm');
    color: $base-80;
    @include xs() {
      margin-bottom: 16px;
    }
  }

  &__badge > .v-chip__content {
    color: $base;
  }
}
</style>
