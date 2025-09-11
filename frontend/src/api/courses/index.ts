import { api } from '@/utils/axios'
import type {
  ICoursesQueryParams,
  IGetCoursesResponse,
  IMyCoursesParams,
  IMyCoursesResponse,
  ICourseDetail,
  IEditorCourse,
} from '@/api/courses/models'
import { ContentTypeEnum } from '@/enums/httpEnum'

enum Api {
  COURSES = '/api/courses/',
  MY_COURSES = '/api/courses/my_courses/',
  MY_COURSES_UPDATE = '/api/courses/my_courses/update/',
  COURSES_TOP_FILTERS_COUNT = '/api/courses/top-filters-count/',
}

const defaultCoursesParams: ICoursesQueryParams = {
  offset: 0,
  limit: 12,
}

export async function getCourses(params?: ICoursesQueryParams): Promise<IGetCoursesResponse> {
  try {
    const response = await api.get(Api.COURSES, {
      params: params ? params : defaultCoursesParams,
      paramsSerializer: {
        indexes: null, // no brackets at all
      },
    })
    return response.data
  } catch (error) {
    console.error('Get courses error:', error)
    throw error
  }
}

export async function getCoursesPrevNextByAPILink(
  queryString: string,
): Promise<IGetCoursesResponse> {
  try {
    const response = await api.get(`${Api.COURSES}?${queryString}`)
    return response.data
  } catch (error) {
    console.error('Get courses error:', error)
    throw error
  }
}

export async function getCourseById(id: string) {
  try {
    const { data } = await api.get<ICourseDetail>(`${Api.COURSES}${id}/`)
    return data
  } catch (error) {
    console.error('Get course error:', error)
    throw error
  }
}

export function postCourse(payload: FormData) {
  return api.post<IEditorCourse>(Api.COURSES, payload, {
    headers: {
      'Content-Type': ContentTypeEnum.FORM_DATA,
    },
  })
}

export function patchCourse(id: string, payload: FormData) {
  return api.patch<IEditorCourse>(`${Api.MY_COURSES_UPDATE}${id}/`, payload, {
    headers: {
      'Content-Type': ContentTypeEnum.FORM_DATA,
    },
  })
}

export async function getMyCourses(params?: IMyCoursesParams): Promise<IMyCoursesResponse> {
  try {
    const response = await api.get(Api.MY_COURSES, {
      params: params ? params : defaultCoursesParams,
      paramsSerializer: {
        indexes: null, // no brackets at all
      },
    })
    return response.data
  } catch (error) {
    console.error('Get my-courses error:', error)
    throw error
  }
}

export async function getCoursesTopFiltersCount(params?: Record<string, string>) {
    try {
      const response = await api.get(Api.COURSES_TOP_FILTERS_COUNT, { params })
      return response.data
    } catch (error) {
      console.error('Get top filters count error:', error)
      throw error
    }
}
