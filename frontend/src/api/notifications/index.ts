import { api } from '@/utils/axios'
import type {
  INotificationsCount,
  INotificationsParams,
  INotificationsReadAll,
  INotificationsResponse,
} from '@/api/notifications/models'

enum Api {
  NOTIFICATIONS = '/api/notifications/',
  NOTIFICATIONS_COUNT = '/api/notifications/count/',
  NOTIFICATIONS_READ_ALL = '/api/notifications/mark_all_as_read/',
  MARK_NOTIFICATION_READ = '/mark_notification_read/',
}

export async function getNotifications(
  params?: INotificationsParams,
): Promise<INotificationsResponse> {
  try {
    const response = await api.get(Api.NOTIFICATIONS, { params })
    return response.data
  } catch (error) {
    console.error('Get notifications error:', error)
    throw error
  }
}

export async function getNotificationsCount(): Promise<INotificationsCount> {
  try {
    const response = await api.get(Api.NOTIFICATIONS_COUNT)
    return response.data
  } catch (error) {
    console.error('Get notifications error:', error)
    throw error
  }
}

export function postReadAllNotifications() {
  return api.post<INotificationsReadAll>(Api.NOTIFICATIONS_READ_ALL)
}

export function patchReadNotificationById(id: number) {
  return api.patch<INotificationsReadAll>(`${Api.NOTIFICATIONS}${id}${Api.MARK_NOTIFICATION_READ}`)
}
