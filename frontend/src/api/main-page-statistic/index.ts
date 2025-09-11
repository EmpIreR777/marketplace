import { api } from '@/utils/axios'
import type { IMainPageStatistic } from '@/api/main-page-statistic/models'

enum Api {
  MAIN_PAGE_STATISTIC = '/api/main_page_statistic/',
}

export async function getMainPageStatistic(): Promise<IMainPageStatistic> {
  try {
    const response = await api.get(Api.MAIN_PAGE_STATISTIC)
    return response.data
  } catch (error) {
    console.error('Get courses error:', error)
    throw error
  }
}
