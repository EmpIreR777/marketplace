import { api } from '@/utils/axios'
import type {
  IUniversitiesQueryParams,
  IUniversityFilterParams,
  IUniversityOrgranization,
  IUniversityOrgranizationListResponse,
  IUniversityProgramFilterParams,
  IUniversityProgramResponse,
} from '@/api/vuz/models'
import type { PaginationParams } from '@/types/index'

enum Api {
  VUZ = '/api/vuz/',
  VUZ_FILTERS = '/api/vuz-filters/',
}

const defaultPaginationParams: PaginationParams = {
  offset: 0,
  limit: 12,
}

export async function getVuz(
  params?: IUniversitiesQueryParams,
): Promise<IUniversityOrgranizationListResponse> {
  try {
    const response = await api.get(Api.VUZ, {
      params: params ? params : defaultPaginationParams,
      paramsSerializer: {
        indexes: null,
      },
    })
    return response.data
  } catch (error) {
    console.error('Get vuz error:', error)
    throw error
  }
}

export async function getVuzById(id: number): Promise<IUniversityOrgranization> {
  try {
    const response = await api.get(`${Api.VUZ}${id}/`)
    return response.data
  } catch (error) {
    console.error('Get vuz error:', error)
    throw error
  }
}

export async function getVuzFilters(params?: IUniversityFilterParams) {
  try {
    const response = await api.get(Api.VUZ_FILTERS, {
      params,
      paramsSerializer: {
        indexes: null,
      },
    })
    return response.data
  } catch (error) {
    console.error('Get vuz filters error:', error)
    throw error
  }
}

export async function getVuzPrograms(
  id: number,
  params?: IUniversitiesQueryParams,
): Promise<IUniversityProgramResponse> {
  try {
    const response = await api.get(`${Api.VUZ}${id}/programs/`, {
      params: params ? params : defaultPaginationParams,
      paramsSerializer: {
        indexes: null,
      },
    })
    return response.data
  } catch (error) {
    console.error('Get vuz programs error:', error)
    throw error
  }
}

export async function getVuzProgramsFilters(
  universityId: number,
  params?: IUniversityProgramFilterParams,
) {
  try {
    const response = await api.get(`${Api.VUZ}${universityId}/programs/filters/`, {
      params,
    })
    return response.data
  } catch (error) {
    console.error('Get vuz filters error:', error)
    throw error
  }
}
