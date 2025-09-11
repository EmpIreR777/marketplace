import type { ICourseCard } from '@/api/courses/models'
import type { IBaseQueryParams, IBaseResponse } from '@/api/models'

export interface IPurchasedCourse {
  id: number
  purchase_date: string
  course: ICourseCard
}

export interface IPurchasedCoursesParams extends IBaseQueryParams {
  ordering?: string
}

export interface PurchasedCoursesResponse extends IBaseResponse {
  results: IPurchasedCourse[]
}
