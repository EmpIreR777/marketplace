import type { UserModule } from '@/types.ts'
import { initYandexMetrika } from 'yandex-metrika-vue3'

export const install: UserModule = ({ app, router }) => {
  const id = import.meta.env.VITE_YANDEX_METRIKA_ID
  if (!id) return

  const metrikaOptions = {
    id,
    router,
    env: import.meta.env.MODE,
    scriptSrc: 'https://mc.yandex.ru/metrika/tag.js' as const,
    defer: true,
    clickmap: true,
    trackLinks: true,
    accurateTrackBounce: true,
    webvisor: true,
  }

  app.use(initYandexMetrika, metrikaOptions)
}
