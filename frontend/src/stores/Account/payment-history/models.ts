import type { IPayment } from "@/api/payments/models";

export interface IPaymentHistoryStoreModel {
  payments: IPayment[]
}
