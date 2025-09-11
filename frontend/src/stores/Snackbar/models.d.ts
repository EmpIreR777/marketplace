import type { IAuthorForFeedback } from '@/api/autor-feedbacks/models'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'

interface ISnackbarAction {
  label: string
  onClick: () => void
}

export interface ISnackbarStoreModel {
  show: boolean
  title: string
  message: string
  type: SnackbarTypeEnum
  timeout: number
  action?: ISnackbarAction | null
}
