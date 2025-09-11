import { MainStatistic } from '@/enums/mainStatisticEnum'

export interface IMainPageStatistic {
  [MainStatistic.COURSES]: number
  [MainStatistic.STUDENTS]: number
  [MainStatistic.AUTHORS]: number
  [MainStatistic.SALES]: number
}
