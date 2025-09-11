import type { IBaseResponse } from '@/api/models'
import type { IBaseQueryParams } from '@/api/models'
import { IFeedbacksParams } from '@/api/feedbacks/models'

interface IFeedbackAuthor {
  id: number
  first_name: string
  last_name: string
  middle_name: string
  photo: string | null
}

interface IFeedbackToCourse {
  id: string
  title: string
}

interface IFeedback {
  id: number
  feedback_author: IFeedbackAuthor
  feedback_text: string
  feedback_rating: number
  time_ago: string
  replies: IFeedback[]
  feedback_to_course: IFeedbackToCourse
  parent_feedback: IFeedback | null
}
export interface IFeedbacksParams extends IBaseQueryParams {
  feedback_to_course?: string
  ordering?: string
}

export interface IFeedbackResponse extends IBaseResponse {
  results: IFeedback[]
}

export interface IPpostFeedback {
  feedback_to_course: string
  feedback_text: string
  feedback_rating: number
  parent_feedback?: number[]
}

export interface IPpostFeedbackResponse extends IPpostFeedback {
  id: number
}

export interface IFeedbacksTopFiltersCountParams {
  top?: string
  learning_types?: string
  course_formats?: string
  courses_thematics?: string
  course_levels?: string
  price_min?: number
  price_max?: number
  organization?: string
  author_types?: string
  minimal_rating?: number
}
