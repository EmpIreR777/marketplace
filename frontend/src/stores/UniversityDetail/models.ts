import type { Recordable } from '@/types'
import type { RouteLocationNormalizedLoadedGeneric, Router } from 'vue-router'
import type { IBaseFilterCatalog } from '@/api/models'
import type { IUniversityOrgranization, IUniversityProgram } from '@/api/vuz/models'

export interface IUniversityDetailStoreModel {
  university: IUniversityOrgranization | null
  renderKey: number
  infinteLoaderData: IUniversityProgram[]
  filtersCatalog: IBaseFilterCatalog | null
  search: string
  ordering: string | null
  filters: Recordable
  isFiltersVisible: boolean
  router: Router
  isLoad: boolean
  route: RouteLocationNormalizedLoadedGeneric
  tabs: Record<string, string>[]
  activeTab: string
}
