import { api } from '@/utils/axios'
import type {
  IFeedbackResponse,
  IFeedbacksParams,
  IFeedbacksTopFiltersCountParams,
  IPpostFeedback,
  IPpostFeedbackResponse,
} from '@/api/feedbacks/models'

enum Api {
  FEEDBACKS = '/api/feedbacks/',
  FEEDBACKS_TOP_FILTER_COUNT = '/api/feedback-top-filters-count/',
}

export async function getFeedbacks(params?: IFeedbacksParams): Promise<IFeedbackResponse> {
  try {
    const response = await api.get(Api.FEEDBACKS, { params })
    return response.data
  } catch (error) {
    console.error('Get courses error:', error)
    throw error
  }
}

export function postFeedback(payload: IPpostFeedback) {
  return api.post<IPpostFeedbackResponse>(Api.FEEDBACKS, payload)
}

export async function getFeedbacksTopFiltersCount(params?: IFeedbacksTopFiltersCountParams) {
  try {
    const response = await api.get(Api.FEEDBACKS_TOP_FILTER_COUNT, { params })
    return response.data
  } catch (error) {
    console.error('Get feedbacks top filters count error:', error)
    throw error
  }
}
