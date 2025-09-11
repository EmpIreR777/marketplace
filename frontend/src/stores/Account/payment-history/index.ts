import { defineStore } from 'pinia'
import type { IPaymentHistoryStoreModel } from '@/stores/Account/payment-history/models'
import { getPayments } from '@/api/payments'
import type { PaginationParams } from '@/types/index'

export const usePaymentHistoryStore = defineStore('paymentHistoryStore', {
  state: (): IPaymentHistoryStoreModel => {
    return {
      payments: [],
    }
  },
  getters: {},
  actions: {
    async loadPayments() {
      const params: PaginationParams = { limit: 12, offset: 0 }
      const { results } = await getPayments(params)
      this.payments = results
    },
  },
})
