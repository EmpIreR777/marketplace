<script setup lang="ts">
import { useDateFormat } from '@vueuse/core'
import type { IPayment } from '@/api/payments/models'
import { StatusEnum, StatusTitle } from '@/enums/statusEnum'
import { PaymentTypeTitle } from '@/enums/paymentEnum'

defineProps<{
  payment: IPayment
}>()
</script>

<template>
  <div v-if="payment" class="payment-history-notification">
    <div class="payment-history-notification__main">
      <div>
        <div class="payment-history-notification__title">{{ payment.amount }} ₽</div>
        <div class="payment-history-notification__date">
          {{ useDateFormat(payment.created_at, 'DD MMMM HH:mm') }}
        </div>
      </div>

      <div>
        <v-chip
          class="payment-history-notification__badge rounded-pill"
          :class="{ completed: payment.status === StatusEnum.COMPLETED }"
          variant="flat"
          label
          size="large"
          density="compact"
        >
          {{ PaymentTypeTitle[payment.payment_type] }} | {{ StatusTitle[payment.status] }}
        </v-chip>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.payment-history-notification {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px 24px;
  border: 1px solid $base-20;
  border-radius: 16px;

  @include xs {
    padding: 16px;
  }

  &.read {
    background-color: $lime-10;
    border-color: $lime-10;
  }

  &__main {
    display: flex;
    justify-content: space-between;
  }

  &__title {
    @include typography('lgb');
  }

  &__date {
    @include typography('sm');
    color: $base-80;
  }

  &__badge {
    @include typography('lg');
    background-color: $base-20;

    &.completed {
      background-color: $lime;
    }

    & .v-chip__content {
      color: $base-80;
    }
  }
}
</style>
