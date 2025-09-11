import type { ITariff, IUserTariff } from '@/api/tariffs/models'
import type { TariffDurationEnum } from '@/enums/tariffs'

export interface ITariffStoreModel {
  tariffs: ITariff[]
  userTariff: IUserTariff | null
  tariffDuration: TariffDurationEnum
  loading: boolean
}
