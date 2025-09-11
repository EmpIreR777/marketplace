import { ICourseItem } from '@/api/courses/models'
import type { IFeedback } from '@/api/feedbacks/models'
import type { IMainPageStatistic } from '@/api/main-page-statistic/models'

export interface IHomeStoreModel {
  courses: ICourseItem[]
  feedbacks: IFeedback[]
  statistic: IMainPageStatistic | null
}
