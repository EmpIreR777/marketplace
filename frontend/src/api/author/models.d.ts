import { AuthorTypeEnum } from '@/enums/userEnum.ts'
import type { IUser } from '@/api/user/models'
import { IAuthor } from '@/api/author/models'
import { ApiLegalForm } from '@/enums/legalTypes'
import type { Recordable } from '@/types'
import { VerificationStatus } from '@/enums/verificationStatuses'

interface IAuthor extends IUser {
  id: number
  author_type: AuthorTypeEnum
  alias: string
  full_title: string
  title: string
  prepositional_title: string
  genitive_title: string
  description: string | null
  logo: string | null
  website: string | null
  address: string | null
  legal_address: string | null
  education_type: string
  is_premium_partner: boolean
  documents: File[]
  is_verified: boolean
  verification_status: VerificationStatus

  // organization: Organization | null
  // name: string
  // is_verified: boolean
  // is_deleted: boolean
  // deletion_reason: string | null
  // phone: string | null
  // email: string | null
}

export interface IAuthorVerify {
  author_type: ApiLegalForm
  verify_fields: Recordable
  documents?: File[]
}
