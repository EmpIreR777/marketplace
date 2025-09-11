import type { IUserProfile } from '@/api/user/models'
import { ICourseItem } from '@/api/courses/models'
import type { AccountTypeEnum } from '@/enums/userEnum.ts'
import type { Router } from 'vue-router'
import { IAuthor } from '@/api/author/models'

export interface IUser {
  id: string
  accessToken: string
  accessTokenDecode: IAccessTokenDecode
  refreshToken: string
  isActivated: boolean
  isAuthenticated: boolean
  uid: string
  resetToken: string
  user: IUserData
  temporaryMail: string
  userProfile: IUserProfile | null
  isVerified: boolean
  isInitialized: boolean
  router: Router
}

interface IUserData {
  id: number | null
  email: string
  account_type: AccountTypeEnum
}

export interface IAccessTokenDecode {
  token_type?: string
  exp?: number
  iat?: number
  jti?: string
  user_id?: number
}
