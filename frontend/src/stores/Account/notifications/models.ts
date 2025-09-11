import type { INotification } from '@/api/notifications/models'

export interface INotificationsStoreModel {
  infinteLoaderData: INotification[]
  notifyCount: number
  isLoading: boolean
  renderKey: number
}
