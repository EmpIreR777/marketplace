import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import type { IUniversitiesStoreModel } from '@/stores/Universities/models'
import { useSnackbarStore } from '@/stores/Snackbar'
import { useInfiniteLoader } from '@/composable/useInfiniteLoader'
import type { Recordable } from '@/types'
import {
  RangeFilterEnum,
  topFiltersCountInitValues,
  type CoursesCategoryEnum,
} from '@/enums/coursesFiltersEnum'
import { getCoursesTopFiltersCount } from '@/api/courses'
import type { InfiniteScrollStatus } from '@/types/index'
import type { IBaseQueryParams, IUniversitiesFilterCatalog } from '@/api/models'
import { getVuz } from '@/api/vuz'
import type { IUniversityOrgranization } from '@/api/vuz/models'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'
import { getVuzFilters } from '@/api/vuz'
import { useFormat } from '@/composable/useFormat'

const { loadData, loadOnScroll, resetLoader } = useInfiniteLoader()

export const useUniversitiesStore = defineStore('universitiesStore', {
  state: (): IUniversitiesStoreModel => {
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
        params.name = state.search
      }

      if (state.topFilters) {
        params.top = state.topFilters
      }

      if (state.ordering) {
        params.ordering = state.ordering
      }

      for (const [key, val] of Object.entries(state.filters)) {
        const isRangeKey = (Object.values(RangeFilterEnum) as string[]).includes(key)

        if (isRangeKey) {
          for (const [rangeType, rangeValue] of Object.entries(val)) {
            params[`${key}_${rangeType}`] = rangeValue
          }
        } else if (val) {
          params[key] = val
        } else {
          delete params[key]
        }
      }

      return params
    },
  },
  actions: {
    async loadUnversitiesFilters() {
      const { formatUniversitiesCatalog } = useFormat()
      const snackbarStore = useSnackbarStore()
      const params = {
        limit: 10,
        offset: 0,
        ...this.getParams,
      }

      try {
        const response = await getVuzFilters(params)
        const formattedCatalog = formatUniversitiesCatalog(response)
        this.setFiltersCatalog(formattedCatalog)

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
    async loadUniversitiesFilterByInnerSearch(
      search: string,
      filter_type: string,
      offset: number,
      isMore?: boolean,
    ) {
      if (!this.filtersCatalog) return
      const { formatUniversitiesCatalog } = useFormat()
      const params = {
        ...this.getParams,
        search,
        filter_type,
        offset,
        limit: 10,
      }
      const response = await getVuzFilters(params)
      const formattedCatalog = formatUniversitiesCatalog(response)

      if (!isMore)
        this.filtersCatalog[filter_type].total_search = formattedCatalog[filter_type].total_search
      this.filtersCatalog[filter_type].items = isMore
        ? [...this.filtersCatalog[filter_type].items, ...formattedCatalog[filter_type].items]
        : formattedCatalog[filter_type].items
    },

    async loadCoursesTopFiltersCount() {
      const response = await getCoursesTopFiltersCount(this.getParams)
      this.topFiltersCount = response
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

    setFilters(data: Recordable<string | number[]>) {
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

    setFilterVisibility(data: boolean) {
      this.isFiltersVisible = data
    },

    pushInfiniteLoaderData(data: IUniversityOrgranization[]) {
      this.infinteLoaderData.push(...data)
    },

    setFiltersCatalog(data: IUniversitiesFilterCatalog | null) {
      this.filtersCatalog = data
    },

    updateRoute() {
      const query: Recordable = {}

      if (this.search) {
        query.name = this.search
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
        if (val && /_min$|_max$/.test(key)) {
          query[key] = val
        } else if (val?.length) {
          query[key] = val.join(',')
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
        } else if (key === 'top') {
          this.topFilters = String(query[key]) as CoursesCategoryEnum
        } else if (key === 'ordering') {
          this.ordering = String(query[key])
        } else if (/_min$|_max$/.test(key)) {
          const [rangeKey, rangeType] = key.split('_')
          if (!this.filters[rangeKey]) {
            this.filters[rangeKey] = {}
          }
          this.filters[rangeKey][rangeType] = Number(query[key])
        } else {
          this.filters[key] = (query[key] as string).split(',')
        }
      }
    },

    async loadInfiniteData(params?: IBaseQueryParams): Promise<InfiniteScrollStatus> {
      const { status, data } = await loadData({
        loader: getVuz,
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

    isRangeFilter(key: string) {
      return (Object.values(RangeFilterEnum) as string[]).includes(key)
    },

    reloadOnScroll() {
      resetLoader()
      this.infinteLoaderData = []
      this.renderKey += 1
    },

    async loadStore() {
      this.loadRouteParams()
      await this.loadUnversitiesFilters()
    },

    clearStore() {
      this.renderKey = 0
      this.infinteLoaderData = []
      this.filtersCatalog = null
      this.search = ''
      this.topFilters = null
      this.topFiltersCount = topFiltersCountInitValues
      this.ordering = null
      this.filters = {}
      this.isFiltersVisible = false
      resetLoader()
    },
  },
})
