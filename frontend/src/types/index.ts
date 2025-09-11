export interface PaginationParams {
  limit?: number
  offset?: number
}

export interface PaginationResponse {
  count: number
  next: string | null
  previous: string | null
}

type NestedItem = {
  title: string
  value: string
}

export type MenuItem = {
  title: string
  value: string
  nested: NestedItem[]
}

export type CourseType = {
  id: number
  image: string
  duration: string
  startDate: string
  title: string
  price: string
}

export type ReviewType = {
  fullName: string
  date: string
  position: string
  rating: number
  text: string
}

export type QuestionnaireItem = {
  id: number // Идентификатор вопроса
  question: string // Текст вопроса
  options: string[]
  isEnd: boolean
}

export interface ICourseMockContent {
  start: string // строка для даты начала
  measurements: [string, string] // массив из двух строк (например, "12 месяцев", "80 занятий")
  tags: string[] // массив строк для тегов
}

export type InfiniteScrollStatus = 'ok' | 'empty' | 'error'

export interface DateRangeModel {
  start_date: Date | null
  end_date: Date | null
}

export interface IInfoItem {
  imgSrc?: string
  icon?: string
  title: string
  text: string
  linkType?: string
}
