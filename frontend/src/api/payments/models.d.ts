import { StatusEnum } from '@/enums/statusEnum.ts'
import type { PaymentTypeEnum } from '@/enums/paymentEnum'
import type { PaginationResponse } from '@/types/index'
import { IPaymentCreate } from './models.d'

export interface getPaymentsResponse extends PaginationResponse {
  results: IPayment[]
}

export interface IPaymentConfirm {
  confirm_url: string
}

export interface IPayment {
  id: number
  item_id: string
  amount: string
  status: StatusEnum
  payment_type: PaymentTypeEnum
  created_at: string
  updated_at: string
  user: number
}

export interface IPaymentCreate {
  item_id: string
  payment_type: string
  amount: string
}

export type IPaymentCreateResponse = IPaymentConfirm | IPayment

export interface IPaymentStatisitcsParams {
  start_date: string
  end_date: string
}

export interface IPaymentStatisitcs {
  best_day: IPayStatBestDay
  best_month: IPayStatBestMonth
  best_year: IPayStatBestYear
  course_stats: IPayStatCorse[]
  purchase_history: IPayStatPurchaseHistory[]
  refund_sales: number
  refund_sum: number
  total_sales: number
  total_sales_day: number
  total_sales_month: number
  total_sales_year: number
  total_sum: number
}

export interface IPayStatBestDay {
  day: string
  total_purchases: number
}
export interface IPayStatBestMonth {
  month: string
  total_purchases: number
}
export interface IPayStatBestYear {
  year: string
  total_purchases: number
}
export interface IPayStatCorse {
  name: string
  total_purchases: number
}
export interface IPayStatPurchaseHistory {
  day: string
  total_purchases: number
}

export interface IPaymentRefund {
  course_id: string
  refund_reason: string
}
