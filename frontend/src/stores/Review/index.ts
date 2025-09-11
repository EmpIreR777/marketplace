import { defineStore } from 'pinia'
import type { OrgReviewsStoreModel } from '@/stores/Review/models'
import type { IAuthorForFeedback } from '@/api/autor-feedbacks/models'
import { getAuthorFeedbackById } from '@/api/autor-feedbacks'
import type { InfiniteScrollStatus } from '@/types/index'
import { useRouter } from 'vue-router'
import { useInfiniteLoader } from '@/composable/useInfiniteLoader'
import type { IBaseQueryParams } from '@/api/models'
import { getFeedbacksByAuthorId } from '@/api/author'
import type { IFeedback, IFeedbackResponse } from '@/api/feedbacks/models'

const { loadData, loadOnScroll, resetLoader } = useInfiniteLoader()

export const useOrgReviewsStore = defineStore('orgReviewsStore', {
  state: (): OrgReviewsStoreModel => {
    return {
      organization: null,
      infinteLoaderData: [],
      router: useRouter(),
      isLoading: false,
    }
  },

  getters: {
    getOrgId(state): number | null {
      return state.router.currentRoute.params?.id
        ? Number(state.router.currentRoute.params?.id)
        : null
    },
  },

  actions: {
    setOrganizations(data: IAuthorForFeedback | null) {
      this.organization = data
    },

    pushInfiniteLoaderData(data: IFeedback[]) {
      this.infinteLoaderData.push(...data)
    },

    async loadOrganization() {
      if (!this.getOrgId) return
      try {
        this.isLoading = true
        const response = await getAuthorFeedbackById(this.getOrgId)
        this.setOrganizations(response)
        return response
      } catch (error) {
        return Promise.reject(error)
      } finally {
        this.isLoading = false
      }
    },

    async loadOrganizationFeedbacks(params?: IBaseQueryParams): Promise<IFeedbackResponse> {
      if (!this.getOrgId) throw new Error('Organization ID is not available')

      const response = await getFeedbacksByAuthorId(this.getOrgId, params)
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
          const status = await this.loadInfiniteData({})
          return { status }
        },
        done,
      })
    },

    clearStore() {
      this.organization = null
      this.infinteLoaderData = []
      resetLoader()
    },
  },
})
