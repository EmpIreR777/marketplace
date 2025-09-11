import type { IAuthorForFeedback } from '@/api/autor-feedbacks/models'
import type { IBaseFilterCatalog } from '@/api/models'
import type { Recordable } from '@/types'
import type { Router } from 'vue-router'
import type { CoursesCategoryEnum } from '@/enums/coursesFiltersEnum'

export interface ReviewsStoreModel {
  renderKey: number
  infinteLoaderData: IAuthorForFeedback[]
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
