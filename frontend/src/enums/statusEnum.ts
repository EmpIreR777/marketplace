export enum StatusEnum {
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  PAID = 'paid',
}

export const StatusTitle = {
  [StatusEnum.PROCESSING]: 'обрабатывается',
  [StatusEnum.COMPLETED]: 'выполнен',
  [StatusEnum.FAILED]: 'провален',
  [StatusEnum.PAID]: 'оплачен',
} as const
