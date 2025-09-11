import { defineStore } from 'pinia'
import { type ITariffStoreModel } from '@/stores/Account/tariff/models'
import { getTariffs, getUserTariff, renewUserTariff, setUserTariff } from '@/api/tariffs'
import { TariffDurationEnum } from '@/enums/tariffs'

export const useTariffStore = defineStore('tariffStore', {
  state: (): ITariffStoreModel => {
    return {
      tariffs: [],
      userTariff: null,
      tariffDuration: TariffDurationEnum.MONTHLY,
      loading: false,
    }
  },

  getters: {},

  actions: {
    async initData() {
      this.loading = true
      try {
        await Promise.all([this.loadTariffs(), this.loadUserTariff()])
      } finally {
        this.loading = false
      }
    },
    async loadTariffs() {
      const data = {
        duration: this.tariffDuration,
      }
      const { results } = await getTariffs(data)
      this.tariffs = results
    },
    async loadUserTariff() {
      const data = await getUserTariff()
      this.userTariff = data
    },
    async changeTariff(id: number) {
      await setUserTariff(id)
      await this.loadUserTariff()
    },
    async renewTariff() {
      const newDate = new Date()
      if (this.tariffDuration === TariffDurationEnum.YEARLY) {
        newDate.setFullYear(newDate.getFullYear() + 1)
      }
      if (this.tariffDuration === TariffDurationEnum.MONTHLY) {
        newDate.setMonth(newDate.getMonth() + 1)
      }

      await renewUserTariff({ expire: newDate.toISOString() })
    },
  },
})
