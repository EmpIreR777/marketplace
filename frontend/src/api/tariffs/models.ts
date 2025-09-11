import type { TariffDurationEnum } from '@/enums/tariffs'
import type { PaginationResponse } from '@/types/index'

export interface ITariff {
  id: number
  name: string
  features: string[]
  price: number
  total_price: number
  discount: number
  percentage: number
}

export interface GetTariffsParams {
  limit?: number
  offset?: number
  duration: TariffDurationEnum
}

export interface GetTariffsResponse extends PaginationResponse {
  results: ITariff[]
}

export interface GetUserTarifResponse {
  tariff: IUserTariff
}

export interface IUserTariff {
  id: string
  tariff: number
  expire: string
  is_timeless: boolean
  is_paid: boolean
}

export interface ITariffRenew {
  expire?: string | null
  is_timeless?: boolean
}

export interface ITariffSet {
  tariff: number
  expire: string
  is_timeless: boolean
  is_paid: boolean
}
