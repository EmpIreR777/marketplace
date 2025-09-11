import type { UserModule } from '@/types.ts'
import { useUser } from '@/stores/User'
import { useNotificationsStore } from '@/stores/Account/notifications'

export const install: UserModule = ({ router }) => {
  router.beforeEach(async (to, from, next) => {
    const userStore = useUser()
    const notificationsStore = useNotificationsStore()

    if (!userStore.isInitialized) {
      await userStore.initApp()
    }
    // console.log('userStore', userStore.getUserProfile?.account_type)
    // Если маршрут требует авторизации и пользователь не аутентифицирован
    if (to.meta.requiresAuth && !userStore.getIsAuthenticated) {
      next('/login') // Перенаправляем на страницу входа
    } else if (to.meta.loadCounter) {
      notificationsStore.loadNotifyCount()
      next() // Разрешаем переход
    } else {
      next() // Разрешаем переход
    }
  })
}
