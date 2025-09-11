import type { IBaseQueryParams, IBaseResponse } from '@/api/models'

export interface INotification {
  id: number
  title: string
  body: number
  html: number
  notification_type: number
  is_read: boolean
  created_at: number
}

export interface INotificationsParams extends IBaseQueryParams {}

export interface INotificationsResponse extends IBaseResponse {
  results: INotification[]
}

export interface INotificationsCount {
  count: number
}

export interface INotificationsReadAll {
  status: strin
  is_success: boolean
}
