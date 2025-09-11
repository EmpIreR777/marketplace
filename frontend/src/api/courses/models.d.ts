import type { IBaseQueryParams, IBaseResponse } from '@/api/models'
import type { IAuthor } from '@/api/author/models'

export interface ICourseBase {
  id: string
  name: string
  link?: string
  course_image?: string
  price?: string
  price_all?: string
  without_discount_price?: string
  price_installment?: string
  time_installment?: number
  course_duration?: number
  is_term_approximately?: boolean
  job_help?: boolean
  job_garant?: boolean
  portfolio_text?: string
  diploma?: boolean
  diploma_content?: string
  mentor?: boolean
  is_webinar?: boolean
  is_top_sale?: boolean
  is_wow_effect?: boolean
  course_description?: string
  organization: string
  learning_types?: number[]
  course_levels?: number[]
  course_formats?: number[]
  courses_thematics?: number[]
  course_targets?: number[]
  author: IOrganizationCourse
  description: string
}

export interface ICourseItem {
  id: string
  organization: string
  comments_count: number
  name: string
  course_image?: string | null
  price: string | null
  course_duration: number | null
  startDate?: string // TO DELETE!!!
}
export interface IGetCoursesResponse {
  count: number
  results: ICourseItem[]
  next: string | null
  previous: string | null
}

export interface IMyCoursesParams extends IBaseQueryParams {
  name?: string
}

export interface IMyCoursesResponse extends IBaseResponse {
  results: ICourseCard[]
}

export interface ICourseCard {
  id: string
  author: string
  price: string
  name: string
  course_image: string
  duration: string | null
  short_descriptions: []
  comments_count: number
  is_active: boolean
  is_moderated: boolean
}

export interface ICoursesQueryParams {
  offset?: number
  limit?: number
  name?: string
  is_webinar?: boolean
  courses_thematics?: string[]
  course_levels?: string[]
  course_formats?: string[]
  course_targets?: string[]
  ordering?: string
  is_top_sale?: boolean
}

export interface IEditorCourse {
  additional_materials?: File[]
  age_category: number[] //
  course_formats: number[] //
  course_images?: (File | string)[]
  images?: (File | string)[] // чтобы не ломать отпарвку файлов отправляем это свойство
  course_levels?: number[]
  course_targets?: number[]
  courses_thematics?: number[]
  date_end?: string | Date | null
  date_start?: string | Date | null
  description?: string | null
  is_active?: boolean
  learning_types: number[]
  link?: string | null
  name: string | null //
  organization?: string
  price?: number | null
  return_conditions?: string | null
  short_descriptions?: IDescr[]
  tag?: string | null
  trial_version?: boolean
}

interface IShortDescription {
  text: string
}

export interface IOrganizationCourse {
  id: number
  email: string
  first_name: string
  last_name: string
  middle_name: string
  photo: string | null
  bio: string | null
  birth_date: string | null // Можно заменить на Date, если парсить дату
  region: string | null
  phone_number: string[] // Исправлено на массив строк
  is_active: boolean
  account_type: number
  author_type: string
  alias: string
  full_title: string
  title: string
  prepositional_title: string
  genitive_title: string
  description: string
  logo: string
  website: string
  address: string
  legal_address: string
  education_type: EducationType
  is_premium_partner: boolean
  documents: any[] // Заменить any на конкретный тип, если известен
}

export interface ICourseDetail {
  id: string
  is_my_course: string
  date_start: string
  date_end: string
  author: IAuthor
  link: string
  learning_types: { id: number; name: string }[]
  name: string
  description: string | null
  course_images: string[]
  course_image: string
  tag: string | null
  course_levels: { id: number; name: string }[]
  course_formats: { id: number; name: string }[]
  courses_thematics: { id: number; name: string }[]
  learning_reasons: { id: number; name: string }[]
  trial_version: boolean
  return_conditions: string | null
  additional_materials: number[]
  age_category: { id: number; name: string }[]
  is_active: boolean
  price: string
  feedbacks_count: string
  is_bought: boolean
  is_returned: boolean
}
