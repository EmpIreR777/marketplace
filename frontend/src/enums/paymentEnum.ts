export enum PaymentTypeEnum {
  SUBSCRIPTION = 'subscription',
  COURSE_PURCHASE = 'course_purchase',
  REFUND = 'refund',
  OTHER = 'other ',
}

export const PaymentTypeTitle = {
  [PaymentTypeEnum.SUBSCRIPTION]: 'подписка',
  [PaymentTypeEnum.COURSE_PURCHASE]: 'покупка',
  [PaymentTypeEnum.REFUND]: 'возврат',
  [PaymentTypeEnum.OTHER]: 'другое',
} as const
