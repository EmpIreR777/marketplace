import { defineStore } from 'pinia'
import type { IAccountStoreModel, IMenuAccount } from './models'
import { AccountTypeEnum } from '@/enums/userEnum.ts'
import { useUser } from '@/stores/User'
import { useNotificationsStore } from '@/stores/Account/notifications'

export const useAccountStore = defineStore('accountStore', {
  state: (): IAccountStoreModel => {
    const notificationsStore = useNotificationsStore()

    return {
      menuItems: [
        {
          title: 'Уведомления',
          icon: 'mdi-bell-outline',
          value: 'notifications',
          count: notificationsStore.notifyCount ?? 0,
        },
        {
          title: 'Статистика',
          icon: 'mdi-poll',
          value: 'statistics',
          roleAccess: [AccountTypeEnum.AUTHOR],
        },
        {
          title: 'Отзывы о курсах',
          icon: 'mdi-creation-outline',
          value: 'my-courses-feedbacks',
          roleAccess: [AccountTypeEnum.AUTHOR],
        },
        {
          title: 'Календарь',
          icon: 'mdi-calendar-month-outline',
          value: 'calendar',
          roleAccess: [AccountTypeEnum.STUDENT],
        },
        {
          title: 'Мои курсы',
          icon: 'mdi-file-swap-outline',
          value: 'my-courses',
          roleAccess: [AccountTypeEnum.AUTHOR],
        },
        {
          title: 'Мои курсы',
          icon: 'mdi-file-swap-outline',
          value: 'purchased-courses',
          roleAccess: [AccountTypeEnum.STUDENT],
        },
        { title: 'Профиль', icon: 'mdi-account-circle-outline', value: 'profile' },
        { title: 'История платежей', icon: 'mdi-credit-card-outline', value: 'payment-history' },
        // {
        //   title: 'Тариф',
        //   icon: 'mdi-star-outline',
        //   value: 'tariff',
        //   roleAccess: [AccountTypeEnum.AUTHOR],
        // },
        { title: 'Выход', icon: 'mdi-logout', value: 'logout' },
      ],
      accountTab: 'courses',
    }
  },

  getters: {
    getAccountTab(): string {
      return this.accountTab
    },
    getMenuItems(): IMenuAccount[] {
      const userStore = useUser()
      const accountType = userStore.getUserProfile?.account_type
      return this.menuItems.filter(
        (item) => !item.roleAccess || (accountType && item.roleAccess.includes(accountType)),
      )
    },
  },
  actions: {
    setAccountTab(tab: string) {
      this.accountTab = tab
    },
  },
})
