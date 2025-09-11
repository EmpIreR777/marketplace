import { api } from '@/utils/axios'
import type { IOrganizationBase } from '@/api/organizations/models'

enum Api {
  ORGANIZATION = 'api/organizations/',
}

export async function getOrganizationById(id: string): Promise<IOrganizationBase> {
  try {
    const response = await api.get(`${Api.ORGANIZATION}${id}`)
    return response.data
  } catch (error) {
    console.error('Get course error:', error)
    throw error
  }
}
