import { defineStore } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import type { IUniversityDetailStoreModel } from '@/stores/UniversityDetail/models'
import { useSnackbarStore } from '@/stores/Snackbar'
import { useInfiniteLoader } from '@/composable/useInfiniteLoader'
import type { Recordable } from '@/types'
import type { InfiniteScrollStatus } from '@/types/index'
import type { IBaseQueryParams } from '@/api/models'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'
import { getVuzById, getVuzPrograms, getVuzProgramsFilters } from '@/api/vuz'
import { getCoursesFilters as getUniversitiesFilters } from '@/api/coursesFilters'
import type { IUniversityProgram } from '@/api/vuz/models'

const { loadData, loadOnScroll, resetLoader } = useInfiniteLoader()

export const useUniversityDetailStore = defineStore('universityDetailStore', {
  state: (): IUniversityDetailStoreModel => {
    return {
      university: null,
      renderKey: 0,
      infinteLoaderData: [],
      filtersCatalog: null,
      search: '',
      ordering: null,
      filters: {},
      isFiltersVisible: false,
      router: useRouter(),
      route: useRoute(),
      isLoad: false,
      tabs: [
        { title: 'Программы', route: '/programs' },
        { title: 'О вузе', route: '/about' },
        { title: 'Оплата', route: '/payment' },
        { title: 'Отзывы', route: '/reviews' },
        { title: 'ЧаВо', route: '/faq' },
      ],
      activeTab: 'programs',
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
    getTabs(state) {
      return state.tabs.map((tab) => ({
        title: tab.title,
        route: `/university-detail/${tab.route.replace('/', '')}`,
      }))
    },

    getSelectedTab(state) {
      const tabRoute = state.route.params.tab || 'programs'
      return tabRoute
    },
  },
  actions: {
    setInitialTab(tab: string) {
      this.activeTab = tab || 'programs'
    },
    async loadUniversity() {
      const universityId = this.route.params.id
      if (!universityId) return
      const university = await getVuzById(+universityId)
      this.university = university
    },
    async loadProgramsFilters() {
      const snackbarStore = useSnackbarStore()
      try {
        const response = await getVuzProgramsFilters(this.university!.id, this.getStringParams)
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

    setFilterVisibility(data: boolean) {
      this.isFiltersVisible = data
    },

    pushInfiniteLoaderData(data: IUniversityProgram[]) {
      this.infinteLoaderData.push(...data)
    },

    setFiltersCatalog(data: any | null) {
      // TODO: type
      this.filtersCatalog = data
    },

    updateRoute() {
      const query: Recordable = {}

      if (this.search) {
        query.title = this.search
      } else {
        delete query.search
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
      this.setInitialTab(this.route.params.tab as string)

      for (const key of Object.keys(query)) {
        if (key === 'title') {
          this.search = String(query[key])
        } else if (key === 'ordering') {
          this.ordering = String(query[key])
        } else {
          this.filters[key] = query[key]
        }
      }
    },
    async loadFiltersCatalog() {
      if (!this.filtersCatalog) {
        try {
          const response = await getUniversitiesFilters(this.getStringParams)
          this.setFiltersCatalog(response)
          return response
        } catch (error) {
          console.error('Ошибка загрузки фильтров:', error)
          return Promise.reject(error)
        }
      }

      return Promise.resolve(this.filtersCatalog)
    },

    async loadInfiniteData(params?: IBaseQueryParams): Promise<InfiniteScrollStatus> {
      const { status, data } = await loadData({
        loader: (params) => getVuzPrograms(this.university!.id, params),
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

    reloadOnScroll() {
      resetLoader()
      this.infinteLoaderData = []
      this.renderKey += 1
    },

    async loadStore() {
      this.loadRouteParams()
      await this.loadUniversity()
      await this.loadProgramsFilters()
    },

    clearStore() {
      this.university = null
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
