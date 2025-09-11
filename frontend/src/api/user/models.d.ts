import { AccountTypeEnum } from '@/enums/userEnum.ts'
import type { IAuthor } from '@/api/author/models'

export interface IUserRegisterBody {
  email: string
  password: string
  re_password: string
  role: number
}

export interface IUserLoginBody {
  email: string
  password: string
}

export interface IUserActivationBody {
  uid: string
  token: string
}

export interface IUserActivationMailBody {
  uid: string
  token: string
  new_email: string
}

export interface IUserChangePassword {
  uid: string
  token: string
  new_password: string
}

export interface ICreateUserResponse {
  email: string
  id: number
}

export interface ITokenResponse {
  message: string
  access_token: string
  refresh_token: string
}

export interface IChangeResponse {
  is_success: boolean
}

export interface ILoginTokenResponse {
  access: string
  refresh: string
}

export interface IUser {
  id: number
  email: string
  first_name: string | null
  last_name: string | null
  middle_name: string | null
  photo: null | string
  bio: string | null
  birth_date: string | null // Можно заменить на Date
  region: string
  phone_number: string | null
  is_active: boolean
  account_type: AccountTypeEnum
}

export type IUserProfile = IUser | IAuthor
