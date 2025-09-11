import { api } from '@/utils/axios'
import type {
  GetTariffsParams,
  GetTariffsResponse,
  GetUserTarifResponse,
  ITariffRenew,
} from '@/api/tariffs/models'

enum Api {
  TARIFFS = '/api/tariffs/',
  USER_TARIFF = '/api/tariffs/user_tariff/',
  USER_TARIFF_SET = '/api/tariffs/user_tariff/set/',
  USER_TARIFF_RENEW = '/api/tariffs/user_tariff/renew/',
}

export async function getTariffs(params: GetTariffsParams) {
  const { data } = await api.get<GetTariffsResponse>(Api.TARIFFS, {
    params: {
      limit: params?.limit || 10,
      offset: params?.offset || 0,
      duration: params.duration,
    },
  })
  return data
}

export async function getUserTariff() {
  const { data } = await api.get<GetUserTarifResponse>(Api.USER_TARIFF)
  return data.tariff
}

export async function setUserTariff(tariff_id: number) {
  const { data } = await api.post(Api.USER_TARIFF_SET, {
    tariff_id,
  })
  return data
}

export async function renewUserTariff(body: ITariffRenew) {
  const { data } = await api.patch(Api.USER_TARIFF_RENEW, body)
  return data
}
