import { api } from '@/utils/axios'
import type { IUserProfile } from '@/api/user/models'
import { ContentTypeEnum } from '@/enums/httpEnum'
import type { IPurchasedCoursesParams, PurchasedCoursesResponse } from '@/api/student/models'
import type { IBaseFilterCatalog, IBaseQueryParams } from '@/api/models'
import type { ICourseDetail } from '@/api/courses/models'

export enum Api {
  STUDENT = '/api/student/{id}/',
  SCHEDULE = '/api/student/get-student-schedule/',
  PURCHASED_COURSES = '/api/student/purchased-courses/',
  PURCHASED_COURSES_FILTERS = '/api/student/purchased-courses-filters/',
}

export async function updateStudent(id: number, body: IUserProfile | FormData) {
  const url = Api.STUDENT.replace('{id}', id.toString())
  const { data } = await api.patch(url, body, {
    headers: {
      'Content-Type': ContentTypeEnum.FORM_DATA,
    },
  })

  return data
}

export async function getStudentSchedule() {
  const response = await api.get(Api.SCHEDULE)
  return response.data
}

export async function getPurchasedCourses(params: IPurchasedCoursesParams) {
  const { data } = await api.get<PurchasedCoursesResponse>(Api.PURCHASED_COURSES, {
    params,
    paramsSerializer: {
      indexes: null,
    },
  })
  return data
}

export async function getPurchasedCourseById(id: string) {
  try {
    const { data } = await api.get<ICourseDetail>(`${Api.PURCHASED_COURSES}${id}/`)
    return data
  } catch (error) {
    console.error('Get course error:', error)
    throw error
  }
}

export async function getPurchasedCoursesFilters(params?: IBaseQueryParams) {
  const { data } = await api.get<IBaseFilterCatalog>(Api.PURCHASED_COURSES_FILTERS, {
    params,
  })
  return data
}
