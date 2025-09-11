import type { UserModule } from '@/types.ts'
import { createGtm, type VueGtmUseOptions } from '@gtm-support/vue-gtm'

export const install: UserModule = ({ app, router }) => {
  const id = import.meta.env.VITE_GTM_ID

  if (!id) return

  const gtmOptions: VueGtmUseOptions = {
    id,
    vueRouter: router,
    debug: true,
  }

  app.use(createGtm(gtmOptions))
}
