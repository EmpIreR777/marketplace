import { defineStore } from 'pinia'
import type { INotificationsStoreModel } from '@/stores/Account/notifications/models'
import type { InfiniteScrollStatus } from '@/types/index'
import {
  getNotifications,
  getNotificationsCount,
  postReadAllNotifications,
  patchReadNotificationById,
} from '@/api/notifications'
import type { INotification } from '@/api/notifications/models'
import type { IBaseQueryParams } from '@/api/models'
import { useInfiniteLoader } from '@/composable/useInfiniteLoader'

const { loadData, loadOnScroll, resetLoader } = useInfiniteLoader()

export const useNotificationsStore = defineStore('notificationsStore', {
  state: (): INotificationsStoreModel => {
    return {
      infinteLoaderData: [],
      renderKey: 0,
      notifyCount: 0,
      isLoading: false,
    }
  },

  getters: {},

  actions: {
    pushInfiniteLoaderData(data: INotification[]) {
      this.infinteLoaderData.push(...data)
    },

    setNotifyCount(val: number) {
      this.notifyCount = val
    },

    async loadNotifyCount() {
      try {
        this.isLoading = true
        const response = await getNotificationsCount()
        this.setNotifyCount(response.count)
        return response
      } catch (error) {
        return Promise.reject(error)
      } finally {
        this.isLoading = false
      }
    },

    async readAllNotifys() {
      try {
        const response = await postReadAllNotifications()
        if (response.data.is_success) {
          this.loadNotifyCount()
          this.reloadOnScroll()
        }
        return response
      } catch (error) {
        return Promise.reject(error)
      }
    },

    async readNotification(id: number) {
      try {
        const response = await patchReadNotificationById(id)
        if (response.data.is_success) {
          this.loadNotifyCount()
          const note = this.infinteLoaderData.find((el) => el.id === id)
          if (note) {
            note.is_read = true
          }
        }
        return response
      } catch (error) {
        return Promise.reject(error)
      }
    },

    async loadInfiniteData(params?: IBaseQueryParams): Promise<InfiniteScrollStatus> {
      const { status, data } = await loadData({
        loader: getNotifications,
        params,
      })

      if (status === 'ok' && data) {
        this.pushInfiniteLoaderData(data)
      }

      return status
    },

    async loadOnScroll({ done }: { done: (status: InfiniteScrollStatus) => void }) {
      return loadOnScroll({
        loader: async () => {
          const status = await this.loadInfiniteData()
          return { status }
        },
        done,
      })
    },

    async reloadOnScroll() {
      resetLoader()
      this.infinteLoaderData = []
      this.renderKey += 1
    },

    clearStore() {
      this.renderKey = 0
      this.infinteLoaderData = []
      resetLoader()
    },
  },
})
