import type {AccountTypeEnum} from "@/enums/userEnum.ts";

export interface IAccountStoreModel {
  accountTab: string
  menuItems: IMenuAccount[]
}

export interface IMenuAccount {
  title: string
  icon: string
  value: string
  count?: number
  roleAccess?: AccountTypeEnum[]
}
