import type { IFeedback } from '@/api/feedbacks/models'

export interface IMyCoursesFeedbacksStoreModel {
  infinteLoaderData: IFeedback[]
  isLoading: boolean
}
