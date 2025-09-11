import { api } from '@/utils/axios'
import type { IGetQuestionnaireResponse } from './models'

enum Api {
  QUESTIONS = '/api/questions/',
}

export async function getQuestions(): Promise<IGetQuestionnaireResponse> {
  try {
    const response = await api.get(Api.QUESTIONS)
    return response.data
  } catch (error) {
    console.error('Get courses error:', error)
    throw error
  }
}
