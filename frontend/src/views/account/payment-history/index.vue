<script setup lang="ts">
import PaymentHistoryNotification from '@/components/account/payment-history/PaymentHistoryNotification.vue';
import { usePaymentHistoryStore } from '@/stores/Account/payment-history'
import { onMounted } from 'vue'

const paymentHistoryStore = usePaymentHistoryStore()

onMounted(() => {
  paymentHistoryStore.loadPayments()
})
</script>

<template>
  <div class="payment-history">
    <div class="text-h5 font-weight-bold d-block d-md-none mb-2">История платежей</div>
    <PaymentHistoryNotification
      v-for="payment in paymentHistoryStore.payments"
      :key="payment.id"
      :payment="payment"
    />
  </div>
</template>

<style scoped>
.payment-history {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
