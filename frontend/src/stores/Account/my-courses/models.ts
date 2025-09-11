import type { Router } from 'vue-router'
import type { ICourseCard } from '@/api/courses/models'
import type { IBaseFilterCatalog } from '@/api/models'
import type { Recordable } from '@/types'

export interface IMyCoursesStoreModel {
  renderKey: number
  infinteLoaderData: ICourseCard[]
  filtersCatalog: IBaseFilterCatalog | null
  search: string
  ordering: string | null
  filters: Recordable
  isFiltersVisible: boolean
  router: Router
  isLoad: boolean
  isLoading: boolean
}
