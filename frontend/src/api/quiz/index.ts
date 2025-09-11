import { api } from '@/utils/axios'
import type {
  // IDeleteAnswersResponse,
  // IQuizQuestion,
  ISavedAnswersResponse,
  ISelectedAnswersBody,
  // IStepBackAnswersResponse,
} from './models'
// import type { IGetCoursesResponse } from '../courses/models'

enum Api {
  QUIZ = '/api/quiz/',
  // QUIZ_BACK = '/api/quiz/back/',
}

// export async function getQuizQuestion(): Promise<IQuizQuestion | IGetCoursesResponse> {
//   try {
//     const response = await api.get(Api.QUIZ)
//     return response.data
//   } catch (error) {
//     console.error('Get courses error:', error)
//     throw error
//   }
// }

export async function postQuizAnswer(body: ISelectedAnswersBody): Promise<ISavedAnswersResponse> {
  try {
    const response = await api.post(Api.QUIZ, body)
    return response.data
  } catch (error) {
    console.error('Get courses error:', error)
    throw error
  }
}

// export async function resetQuizQuestions(): Promise<{
//   data: IDeleteAnswersResponse
//   status: number
// }> {
//   try {
//     const response = await api.delete(Api.QUIZ)
//     return { data: response.data, status: response.status }
//   } catch (error) {
//     console.error('Get courses error:', error)
//     throw error
//   }
// }

// export async function postStepBackQuizQuestion(): Promise<IStepBackAnswersResponse> {
//   try {
//     const response = await api.post(Api.QUIZ_BACK)
//     return response.data
//   } catch (error) {
//     console.error('Get courses error:', error)
//     throw error
//   }
// }
