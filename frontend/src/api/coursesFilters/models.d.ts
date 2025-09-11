import { FILTER_PROPERTIES_NAMES } from './constants'
import type { IOption } from '@/api/models'

export interface IFilterProperties {
  // Courses
  [FILTER_PROPERTIES_NAMES.thematics]?: IFilterItem[]
  [FILTER_PROPERTIES_NAMES.age_category]: IOption[]
  [FILTER_PROPERTIES_NAMES.course_formats]: IOption[]
  [FILTER_PROPERTIES_NAMES.course_levels]: IOption[]
  [FILTER_PROPERTIES_NAMES.course_targets]: IOption[]
  [FILTER_PROPERTIES_NAMES.courses_thematics]: IOption[]
  [FILTER_PROPERTIES_NAMES.learning_types]: IOption[]
  // Universities
  [FILTER_PROPERTIES_NAMES.cities]: IOption[]
  [FILTER_PROPERTIES_NAMES.faculties]: IOption[]
  [FILTER_PROPERTIES_NAMES.forms]: IOption[]
  [FILTER_PROPERTIES_NAMES.metros]: IOption[]
  [FILTER_PROPERTIES_NAMES.rating]: IRatingRange
  [FILTER_PROPERTIES_NAMES.specialties]: IOption[]
  [FILTER_PROPERTIES_NAMES.subjects]: IOption[]
  // Utils
  [FILTER_PROPERTIES_NAMES.price]: IPriceRange
}

export interface IFilterItem {
  name: string
}

export interface IPriceRange {
  [FILTER_PROPERTIES_NAMES.price_min]: number
  [FILTER_PROPERTIES_NAMES.price_max]: number
}

export interface IRatingRange {
  [FILTER_PROPERTIES_NAMES.rating_min]: number
  [FILTER_PROPERTIES_NAMES.rating_max]: number
}
