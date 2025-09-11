import type { IFilterProperties } from '@/api/coursesFilters/models'
import type { Router } from 'vue-router'
import type { ICourseDetail } from '@/api/courses/models'
import type { IFeedback } from '@/api/feedbacks/models'

export interface ICourseStoreModel {
  course: ICourseDetail | null
  originCourse: ICourseDetail | null
  isLoading: boolean
  filtersCatalog: IFilterProperties | null
  router: Router
  feedbacks: IFeedback[]
  isReportDialog: boolean
  isRefundDialog: boolean
}

export interface IPartialEditorCourse extends Partial<ICourseCreate> {}
