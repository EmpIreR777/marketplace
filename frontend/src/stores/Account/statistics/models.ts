import type { IPaymentStatisitcs } from '@/api/payments/models'
import type { PeriodEnum } from '@/enums/periodEnum'
import type { Router } from 'vue-router'

export interface IStatisticsStoreModel {
  statistics: IPaymentStatisitcs | null
  chartData: ChartData[]
  areaSeries: number[]
  areaCategories: string[]
  start_date: Date | null
  end_date: Date | null
  periodFilter: PeriodEnum | null
  isLoading: boolean
  router: Router
}

interface ChartData {
  x: string
  y: number
}
