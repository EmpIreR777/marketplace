import { api } from '@/utils/axios'
import type { IUserProfile } from '@/api/user/models'
import { ContentTypeEnum } from '@/enums/httpEnum'
import type { IBaseQueryParams } from '@/api/models'
import type { IFeedbackResponse } from '@/api/feedbacks/models'
import type { IAuthorVerify } from '@/api/author/models'
import { useFormData } from '@/composable/useFormData'

export enum Api {
  AUTHOR = '/api/author/{id}/',
  AUTHOR_FEEDBACKS = '/api/author/{id}/feedbacks/',
}

export async function updateAuthor(id: number, body: IUserProfile | FormData) {
  const url = Api.AUTHOR.replace('{id}', id.toString())
  const { data } = await api.patch(url, body, {
    headers: {
      'Content-Type': ContentTypeEnum.FORM_DATA,
    },
  })

  return data
}

export async function getFeedbacksByAuthorId(
  id: number,
  params?: IBaseQueryParams,
): Promise<IFeedbackResponse> {
  const url = Api.AUTHOR_FEEDBACKS.replace('{id}', id.toString())
  try {
    const response = await api.get(url, {
      params,
      paramsSerializer: {
        indexes: null,
      },
    })
    return response.data
  } catch (error) {
    console.error('Get FeedbacksByAuthorId error:', error)
    throw error
  }
}

export function patchAuthorVerify(id: number, payload: IAuthorVerify) {
  const url = Api.AUTHOR.replace('{id}', id.toString())
  const formData = useFormData(payload)

  return api.patch<unknown>(url, formData, {
    headers: {
      'Content-Type': ContentTypeEnum.FORM_DATA,
    },
  })
}
