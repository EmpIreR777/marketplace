import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import type { IMyCoursesStoreModel } from '@/stores/Account/my-courses/models'
import type { InfiniteScrollStatus } from '@/types/index'
import type { ICourseCard } from '@/api/courses/models'
import type { IBaseFilterCatalog, IBaseQueryParams } from '@/api/models'
import { useInfiniteLoader } from '@/composable/useInfiniteLoader'
import { getMyCourses } from '@/api/courses'
import type { Recordable } from '@/types'
import { getMyCoursesFilters } from '@/api/coursesFilters'
import { useSnackbarStore } from '@/stores/Snackbar'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'

const { loadData, loadOnScroll, resetLoader, state } = useInfiniteLoader()

export const useMyCoursesStore = defineStore('myCoursesStore', {
  state: (): IMyCoursesStoreModel => {
    return {
      renderKey: 0,
      infinteLoaderData: [],
      filtersCatalog: null,
      search: '',
      ordering: null,
      filters: {},
      isFiltersVisible: false,
      router: useRouter(),
      isLoad: false,
      isLoading: false,
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
        params.name = state.search
      }

      if (state.ordering) {
        params.ordering = state.ordering
      }

      for (const [key, val] of Object.entries(this.filters)) {
        if (val && (val > 0 || val.length > 0)) {
          params[key] = val
        } else {
          delete params[key]
        }
      }

      return params
    },
  },

  actions: {
    async loadMyCoursesFilters() {
      const snackbarStore = useSnackbarStore()
      const stringParams: Record<string, string> = {}

      for (const [key, value] of Object.entries(this.getParams)) {
        if (Array.isArray(value)) {
          stringParams[key] = value.join(',')
        } else {
          stringParams[key] = String(value)
        }
      }
      try {
        const response = await getMyCoursesFilters(stringParams)
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

    pushInfiniteLoaderData(data: ICourseCard[]) {
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

    setFilters(data: Recordable<string[] | number[]>) {
      Object.entries(data).forEach(([key, value]) => {
        this.filters[key] = value
      })
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
        query.name = this.search
      }

      if (this.ordering) {
        query.ordering = this.ordering
      } else {
        delete query.ordering
      }

      for (const [key, val] of Object.entries(this.filters)) {
        if (val && (val > 0 || val.length > 0)) {
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
        if (key === 'name') {
          this.search = String(query[key])
        } else if (key === 'ordering') {
          this.ordering = String(query[key])
        } else {
          this.filters[key] = query[key]
        }
      }
    },

    async loadInfiniteData(params?: IBaseQueryParams): Promise<InfiniteScrollStatus> {
      const { status, data } = await loadData({
        loader: getMyCourses,
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
      await this.loadMyCoursesFilters()
    },

    clearStore() {
      this.renderKey = 0
      this.infinteLoaderData = []
      this.filtersCatalog = null
      this.search = ''
      this.ordering = null
      this.filters = {}
      this.isFiltersVisible = false
      resetLoader()
    },
  },
})
