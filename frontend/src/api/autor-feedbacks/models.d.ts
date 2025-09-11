import type { IBaseResponse } from '@/api/models'

export interface IAuthorForFeedback {
  full_title: string
  id: number
  legal_address: string
  logo: string
  title: string
  total_feedbacks: number
  total_rating: number
}

export interface IAuthorForFeedbacksResponse extends IBaseResponse {
  results: IAuthorForFeedback[]
}
