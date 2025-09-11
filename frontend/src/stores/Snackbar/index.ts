// stores/snackbarStore.js
import { defineStore } from 'pinia'
import type { ISnackbarStoreModel } from '@/stores/Snackbar/models'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'

export const useSnackbarStore = defineStore('snackbarStore', {
  state: (): ISnackbarStoreModel => ({
    show: false,
    title: '',
    message: '',
    type: SnackbarTypeEnum.DEFAULT,
    timeout: 3000,
    action: null,
  }),
  actions: {
    showSnackbar(options: {
      title?: string
      message?: string
      type?: SnackbarTypeEnum
      timeout?: number
      action?: { label: string; onClick: () => void }
    }) {
      this.title = options.title || ''
      this.message = options.message || ''
      this.type = options.type || SnackbarTypeEnum.DEFAULT
      this.timeout = options.timeout || 3000
      this.action = options.action || null
      this.show = true

      setTimeout(() => {
        this.hideSnackbar()
      }, this.timeout)
    },
    hideSnackbar() {
      this.show = false
    },
  },
})
