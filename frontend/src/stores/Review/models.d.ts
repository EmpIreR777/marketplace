import type { IFeedback } from '@/api/feedbacks/models'
import type { IAuthorForFeedback } from '@/api/autor-feedbacks/models'
import type { Router } from 'vue-router'

export interface OrgReviewsStoreModel {
  infinteLoaderData: IFeedback[]
  organization: IAuthorForFeedback | null
  router: Router
  isLoading: boolean
}
