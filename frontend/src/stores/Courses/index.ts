import { nextTick } from 'vue'
import { defineStore } from 'pinia'
import type { ICoursesStoreModel } from './models'
import { getCourses, getCoursesTopFiltersCount } from '@/api/courses'
import type { ICourseItem, ICoursesQueryParams } from '@/api/courses/models'
import type { InfiniteScrollStatus } from '@/types/index'
import { useRouter, type RouteLocationNormalizedLoadedGeneric } from 'vue-router'
import type { Recordable } from '@/types'
import { getCoursesFilters } from '@/api/coursesFilters'
import type { IBaseFilterCatalog, IBaseQueryParams } from '@/api/models'
import { useInfiniteLoader } from '@/composable/useInfiniteLoader'
import { CoursesCategoryEnum, topFiltersCountInitValues } from '@/enums/coursesFiltersEnum'
import { useSnackbarStore } from '@/stores/Snackbar'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'

const { loadData, loadOnScroll, resetLoader, state } = useInfiniteLoader()

export const useCoursesStore = defineStore('coursesStore', {
  state: (): ICoursesStoreModel => {
    return {
      courses: [],
      offset: 0,
      limit: 12,
      loading: false,
      isScrollActive: true,

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
    getCoursesList(state) {
      return state.courses
    },
    getOthetAuthorCourses(state) {
      return (id: string) => {
        return this.courses.filter((course) => course.id !== id)
      }
    },
    // NEW CODE FROM PURCHASED COURSES STORE
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
  },

  actions: {
    async loadMoreCourses(
      done: (status: InfiniteScrollStatus) => void,
      route: RouteLocationNormalizedLoadedGeneric,
    ) {
      try {
        const params = {
          limit: this.limit,
          offset: this.offset,
          ...route.query,
        }
        const { results, count } = await getCourses(params)
        this.courses = [...this.courses, ...results]
        this.offset += this.limit

        if (this.offset >= count) {
          done('empty')
        } else {
          done('ok')
        }
      } catch (err) {
        done('error')
      }
    },
    async loadCoursesTopFiltersCount() {
      const response = await getCoursesTopFiltersCount(this.getStringParams)
      this.topFiltersCount = response
    },
    resetCoursesScroll() {
      this.isScrollActive = false
      nextTick(() => {
        this.isScrollActive = true
      })
    },
    clearCourses() {
      this.offset = 0
      this.courses = []
      this.resetCoursesScroll()
    },
    async loadCoursesList(params?: ICoursesQueryParams) {
      try {
        const response = await getCourses(params)
        this.setCoursesList(response.results)
        this.offset += 12
        return response
      } catch (error) {
        // TODO notify: show error message
        return Promise.reject(error)
      }
    },
    setCoursesList(data: ICourseItem[]) {
      this.courses = data
    },
    setNextPageData(data: ICourseItem[]) {
      this.courses = [...this.courses, ...data]
    },
    setLoading(data: boolean) {
      this.loading = data
    },
    // NEW CODE
    async loadCoursesFilters() {
      const snackbarStore = useSnackbarStore()
      try {
        const response = await getCoursesFilters(this.getStringParams)
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
      await Promise.all([this.loadCoursesFilters(), this.loadCoursesTopFiltersCount()])
    },

    pushInfiniteLoaderData(data: ICourseItem[]) {
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
        query.name = this.search
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
        loader: getCourses,
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
