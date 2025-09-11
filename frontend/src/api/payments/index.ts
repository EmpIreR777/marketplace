import { api } from '@/utils/axios'
import type {
  getPaymentsResponse,
  IPayment,
  IPaymentCreate,
  IPaymentCreateResponse,
  IPaymentRefund,
  IPaymentStatisitcs,
  IPaymentStatisitcsParams,
} from '@/api/payments/models'
import type { PaginationParams } from '@/types/index'

export enum Api {
  PAYMENTS = '/api/payments/',
  PAYMENTS_STATISTICS = '/api/payments/statistics/',
  PAYMENTS_REFUND = '/api/payments/refund/',
}

export async function getPayments(params?: PaginationParams) {
  const { data } = await api.get<getPaymentsResponse>(Api.PAYMENTS, { params })
  return data
}

export async function createPayments(data?: IPaymentCreate) {
  const res = await api.post<IPaymentCreateResponse>(Api.PAYMENTS, data)
  return res.data
}

export async function getPaymentsStatistics(params?: IPaymentStatisitcsParams) {
  const { data } = await api.get<IPaymentStatisitcs>(Api.PAYMENTS_STATISTICS, { params })
  return data
}

export async function createRefund(payload: IPaymentRefund) {
  const res = await api.post<IPayment>(Api.PAYMENTS_REFUND, payload)
  return res.data
}
