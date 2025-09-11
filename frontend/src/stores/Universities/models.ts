import type { Recordable } from '@/types'
import type { Router } from 'vue-router'
import type { IUniversitiesFilterCatalog } from '@/api/models'
import type { CoursesCategoryEnum } from '@/enums/coursesFiltersEnum'
import type { IUniversityOrgranization } from '@/api/vuz/models'

export interface IUniversitiesStoreModel {
  renderKey: number
  infinteLoaderData: IUniversityOrgranization[]
  filtersCatalog: IUniversitiesFilterCatalog | null
  search: string
  topFilters: CoursesCategoryEnum | null
  topFiltersCount: Record<CoursesCategoryEnum, number>
  ordering: string | null
  filters: Recordable
  isFiltersVisible: boolean
  router: Router
  isLoad: boolean
}
