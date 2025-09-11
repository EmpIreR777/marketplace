import type { IPurchasedCourse } from '@/api/student/models'
import type { Recordable } from '@/types'
import type { Router } from 'vue-router'
import type { IBaseFilterCatalog } from '@/api/models'

export interface IPurchasedCoursesStoreModel {
  renderKey: number
  infinteLoaderData: IPurchasedCourse[]
  filtersCatalog: IBaseFilterCatalog | null
  search: string
  ordering: string | null
  filters: Recordable
  isFiltersVisible: boolean
  router: Router
  isLoad: boolean
  // Title
  coursesListType: 'куплено' | 'отфильтровано'
  coursesCounter: number
}
