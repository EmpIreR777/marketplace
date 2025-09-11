import type { Router } from 'vue-router'
import type { ICourseItem } from '@/api/courses/models'
import type { IBaseFilterCatalog } from '@/api/models'
import type { Recordable } from '@/types'
import { CoursesCategoryEnum } from '@/enums/coursesFiltersEnum'

export interface ICoursesStoreModel {
  courses: ICourseItem[]
  offset: number
  limit: number
  loading: boolean
  isScrollActive: boolean

  renderKey: number
  infinteLoaderData: ICourseItem[]
  filtersCatalog: IBaseFilterCatalog | null
  search: string
  topFilters: CoursesCategoryEnum | null
  topFiltersCount: Record<CoursesCategoryEnum, number>
  ordering: string | null
  filters: Recordable
  isFiltersVisible: boolean
  router: Router
  isLoad: boolean
}
