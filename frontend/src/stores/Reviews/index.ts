import { defineStore } from 'pinia'
import type { ReviewsStoreModel } from '@/stores/Reviews/models'
import type { IAuthorForFeedback } from '@/api/autor-feedbacks/models'
import { getAuthorFeedbacks } from '@/api/autor-feedbacks'
import type { InfiniteScrollStatus } from '@/types/index'
import { useInfiniteLoader } from '@/composable/useInfiniteLoader'
import type { IBaseFilterCatalog, IBaseQueryParams } from '@/api/models'
import { getAuthorFilters } from '@/api/coursesFilters'
import type { Recordable } from '@/types'
import { useRouter } from 'vue-router'
import { topFiltersCountInitValues, CoursesCategoryEnum } from '@/enums/coursesFiltersEnum'
import { useSnackbarStore } from '@/stores/Snackbar'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'
import { getFeedbacksTopFiltersCount } from '@/api/feedbacks'

const { loadData, loadOnScroll, resetLoader } = useInfiniteLoader()

export const useReviewsStore = defineStore('reviewsStore', {
  state: (): ReviewsStoreModel => {
    return {
      renderKey: 0,
      infinteLoaderData: [],
      filtersCatalog: null,
      search: '',
      topFilters: null,
      topFiltersCount: topFiltersCountInitValues,
      ordering: null,
      filters: {},
      isFiltersVisible: false,
      router: useRouter(),
      isLoad: false,
    }
  },

  getters: {
    getFiltersCatalog(state) {
      return state.filtersCatalog
    },

    getActiveFiltersCount(state) {
      return Object.values(state.filters ?? {}).reduce((count, value) => {
        if (Array.isArray(value)) {
          return count + value.length
        } else if (value !== null && value !== undefined && value !== '') {
          return count + 1
        }
        return count
      }, 0)
    },

    getParams(state) {
      const params: Recordable = {}

      if (state.search) {
        params.title = state.search
      }

      if (state.topFilters) {
        params.top = state.topFilters
      } else {
        delete params.top
      }

      if (state.ordering) {
        params.ordering = state.ordering
      }

      for (const [key, val] of Object.entries(this.filters)) {
        if (val.length > 0) {
          params[key] = val
        } else {
          delete params[key]
        }
      }

      return params
    },

    getStringParams() {
      const stringParams: Record<string, string> = {}

      for (const [key, value] of Object.entries(this.getParams)) {
        if (Array.isArray(value)) {
          stringParams[key] = value.join(',')
        } else {
          stringParams[key] = String(value)
        }
      }

      return stringParams
    },
  },

  actions: {
    async loadCoursesFilters() {
      const snackbarStore = useSnackbarStore()

      try {
        const response = await getAuthorFilters(this.getStringParams)
        this.setFiltersCatalog(response)

        return response
      } catch (error) {
        snackbarStore.showSnackbar({
          title: 'Ошибка загрузки фильтров',
          message: 'Попробуйте обновить страницу или повторить попытку позже.',
          type: SnackbarTypeEnum.NEGATIVE,
          action: { label: 'Закрыть', onClick: () => (snackbarStore.show = false) },
        })
        return Promise.reject(error)
      }
    },

    async updateFilters() {
      await Promise.all([this.loadCoursesFilters(), this.loadReviewsTopFiltersCount()])
    },

    async loadReviewsTopFiltersCount() {
      const response = await getFeedbacksTopFiltersCount(this.getStringParams)
      this.topFiltersCount = response
    },

    pushInfiniteLoaderData(data: IAuthorForFeedback[]) {
      this.infinteLoaderData.push(...data)
    },

    setFiltersCatalog(data: IBaseFilterCatalog | null) {
      this.filtersCatalog = data
    },

    setFilterVisibility(data: boolean) {
      this.isFiltersVisible = data
    },

    setSearch(value: string) {
      this.search = value
      this.updateRoute()
      this.reloadOnScroll()
    },

    setOrdering(value: string | null) {
      this.ordering = value

      this.updateRoute()
      this.reloadOnScroll()
    },

    setFilters(data: Recordable<string[]>) {
      Object.entries(data).forEach(([key, value]) => {
        this.filters[key] = value
      })
      this.updateRoute()
      this.reloadOnScroll()
    },

    setTopFilters(data: CoursesCategoryEnum) {
      this.topFilters = this.topFilters === data ? null : data
      this.updateRoute()
      this.reloadOnScroll()
    },

    resetFilters() {
      this.filters = {}
      this.updateRoute()
      this.reloadOnScroll()
    },

    updateRoute() {
      const query: Recordable = {}

      if (this.search) {
        query.search = this.search
      } else {
        delete query.search
      }

      if (this.topFilters) {
        query.top = this.topFilters
      } else {
        delete query.top
      }

      if (this.ordering) {
        query.ordering = this.ordering
      } else {
        delete query.ordering
      }

      for (const [key, val] of Object.entries(this.filters)) {
        if (val.length > 0) {
          query[key] = val
        } else {
          delete query[key]
        }
      }

      this.router.replace({ query })
    },

    loadRouteParams(): void {
      const query = this.router.currentRoute.query

      for (const key of Object.keys(query)) {
        if (key === 'search') {
          this.search = String(query[key])
        } else if (key === 'top') {
          this.topFilters = String(query[key]) as CoursesCategoryEnum
        } else if (key === 'ordering') {
          this.ordering = String(query[key])
        } else {
          this.filters[key] = query[key]
        }
      }
    },

    async loadInfiniteData(params?: IBaseQueryParams): Promise<InfiniteScrollStatus> {
      const { status, data } = await loadData({
        loader: getAuthorFeedbacks,
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
          const status = await this.loadInfiniteData(this.getParams)
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

    async loadStore() {
      this.loadRouteParams()
      await this.updateFilters()
    },

    clearStore() {
      this.renderKey = 0
      this.infinteLoaderData = []
      this.filtersCatalog = null
      resetLoader()
    },
  },
})
