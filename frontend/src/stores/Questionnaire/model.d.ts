import { type IQuestion } from '@/api/questionnaire/IQuestion'
import { type IQuizQuestion } from '@/api/quiz/models'

export interface IQuestionnaireStoreModel {
  questionnaireQuestions: IQuestion[] | null
  currentQuestion: number | null
  answersResults: Record<number, number[]> | null
  questionnaireQuizQuestions: IQuizQuestion[] | null
  isLastQuestion: boolean
}

export interface IAanswersResult {
  stepId: number
  answers: number[]
}
