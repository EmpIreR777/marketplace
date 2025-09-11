import { defineStore } from 'pinia'
import type { IMyCoursesFeedbacksStoreModel } from '@/stores/Account/my-courses-feedbacks/models'
import type { InfiniteScrollStatus } from '@/types/index'
import type { IBaseQueryParams } from '@/api/models'
import { useInfiniteLoader } from '@/composable/useInfiniteLoader'
import { useUser } from '@/stores/User'
import { getFeedbacksByAuthorId } from '@/api/author'
import type { IFeedback, IFeedbackResponse } from '@/api/feedbacks/models'

const userStore = useUser()
const { loadData, loadOnScroll, resetLoader } = useInfiniteLoader()

export const useMyCoursesFeedbacksStore = defineStore('myCoursesFeedbacksStore', {
  state: (): IMyCoursesFeedbacksStoreModel => {
    return {
      infinteLoaderData: [],
      isLoading: false,
    }
  },

  getters: {},

  actions: {
    pushInfiniteLoaderData(data: IFeedback[]) {
      this.infinteLoaderData.push(...data)
    },

    async loadOrganizationFeedbacks(params?: IBaseQueryParams): Promise<IFeedbackResponse> {
      const userId = Number(userStore.getUserId)

      const response = await getFeedbacksByAuthorId(userId, params)
      if (!response) throw new Error('No response received')

      return response
    },

    async loadInfiniteData(params?: IBaseQueryParams): Promise<InfiniteScrollStatus> {
      const { status, data } = await loadData({
        loader: this.loadOrganizationFeedbacks,
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

    clearStore() {
      this.infinteLoaderData = []
      resetLoader()
    },
  },
})
