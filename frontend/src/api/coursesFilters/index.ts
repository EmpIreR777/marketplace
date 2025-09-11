import { api } from '@/utils/axios'
import type { IBaseFilterCatalog } from '../models'

enum Api {
  COURSES_FILTERS = '/api/courses-filters/',
  MY_COURSES_FILTERS = '/api/my-courses-filters/',
  AUTHOR_FILTERS = '/api/author-filters/',
}

export async function getCoursesFilters(
  params?: Record<string, string>,
): Promise<IBaseFilterCatalog> {
  try {
    const response = await api.get(Api.COURSES_FILTERS, { params })
    return response.data
  } catch (error) {
    console.error('Get courses filters error:', error)
    throw error
  }
}

export async function getMyCoursesFilters(
  params?: Record<string, string>,
): Promise<IBaseFilterCatalog> {
  try {
    const response = await api.get(Api.MY_COURSES_FILTERS, { params })
    return response.data
  } catch (error) {
    console.error('Get my courses filters error:', error)
    throw error
  }
}

export async function getAuthorFilters(params?: Record<string, string>) {
  try {
    const response = await api.get(Api.AUTHOR_FILTERS, { params })
    return response.data
  } catch (error) {
    console.error('Get author filters error:', error)
    throw error
  }
}
