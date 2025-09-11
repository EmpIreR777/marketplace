import { api } from '@/utils/axios'
import type { IAuthorForFeedback, IAuthorForFeedbacksResponse } from '@/api/autor-feedbacks/models'
import type { IBaseQueryParams } from '@/api/models'

enum Api {
  AUTHOR_FEEDBACKS = '/api/author-top-by-feedbacks/',
}

export async function getAuthorFeedbacks(
  params?: IBaseQueryParams,
): Promise<IAuthorForFeedbacksResponse> {
  try {
    const response = await api.get(Api.AUTHOR_FEEDBACKS, {
      params,
      paramsSerializer: {
        indexes: null,
      },
    })
    return response.data
  } catch (error) {
    console.error('Get AuthorFeedbacks error:', error)
    throw error
  }
}

export async function getAuthorFeedbackById(id: number): Promise<IAuthorForFeedback> {
  try {
    const response = await api.get(`${Api.AUTHOR_FEEDBACKS}${id}/`)
    return response.data
  } catch (error) {
    console.error('Get AuthorFeedbackById error:', error)
    throw error
  }
}
