import type { IOrganizationBase } from "@/api/organizations/models";


export interface IOrganizationStoreModel {
  course: IOrganizationBase | null
  isLoading: boolean
}
