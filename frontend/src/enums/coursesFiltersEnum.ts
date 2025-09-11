import { FILTER_PROPERTIES_NAMES } from '@/api/coursesFilters/constants'

export enum SORTING_FIELDS {
  PRICE = 'PRICE',
  POPULARITY = 'POPULARITY',
  RATING = 'RATING',
  PURCHASE_DATE = 'PURCHASE_DATE',
}

export const SORTING_FIELDS_TRANSLATE = {
  [SORTING_FIELDS.PRICE]: 'Цена',
  [SORTING_FIELDS.POPULARITY]: 'Популярность',
  [SORTING_FIELDS.RATING]: 'Рейтинг',
  [SORTING_FIELDS.PURCHASE_DATE]: 'Дата покупки',
} as const

export const SORTING_API_FIELDS = {
  [SORTING_FIELDS.PRICE]: 'price',
} as const

export enum SortingDirectionEnum {
  ASC = '-',
  DESC = '',
}

export enum RangeFilterEnum {
  PRICE = 'price',
  RATING = 'rating',
}

export const FILTER_PROPERTIES_TITLES = {
  [FILTER_PROPERTIES_NAMES.thematics]: 'Специализация',
  [FILTER_PROPERTIES_NAMES.learning_types]: 'Направления',
  [FILTER_PROPERTIES_NAMES.courses_thematics]: 'Специализация',
  [FILTER_PROPERTIES_NAMES.price]: 'Стоимость',
  [FILTER_PROPERTIES_NAMES.course_formats]: 'Формат обучения',
  [FILTER_PROPERTIES_NAMES.course_levels]: 'Уровни',
  [FILTER_PROPERTIES_NAMES.age_category]: 'Возрастная категория',
  [FILTER_PROPERTIES_NAMES.course_targets]: 'Цель',
  [FILTER_PROPERTIES_NAMES.author_types]: 'Тип автора',

  [FILTER_PROPERTIES_NAMES.city]: 'Город',
  [FILTER_PROPERTIES_NAMES.faculty]: 'Факультет',
  [FILTER_PROPERTIES_NAMES.form]: 'Форма обучения',
  [FILTER_PROPERTIES_NAMES.metro]: 'Станция метро',
  [FILTER_PROPERTIES_NAMES.rating]: 'Рейтинг',
  [FILTER_PROPERTIES_NAMES.specialty]: 'Специальность',
  [FILTER_PROPERTIES_NAMES.subject]: 'Регион',
  [FILTER_PROPERTIES_NAMES.level_code]: 'Уровень образования',
  [FILTER_PROPERTIES_NAMES.organization_type]: 'Тип учебного заведения',
  [FILTER_PROPERTIES_NAMES.is_state]: 'Форма собственности',
} as const

export const FILTER_CHECKBOX_VISIBLE_COUNT = 5

export const API_ORDERING_KEYS = {
  [SORTING_FIELDS.POPULARITY]: 'total_feedbacks',
  [SORTING_FIELDS.RATING]: 'total_rating',
  [SORTING_FIELDS.PURCHASE_DATE]: 'purchase_date',
} as const

export const ORDERING_OPTIONS = [
  { apiKey: 'name', label: 'Название' },
  { apiKey: 'price', label: 'Цена' },
  { apiKey: 'date_start', label: 'Дата начала' },
]

export enum CoursesCategoryEnum {
  SCHOOL = 'school',
  ONLINE = 'online',
  OFFLINE = 'offline',
  UNIVERSITY = 'university',
  TRAINING = 'training',
  LANGUAGE = 'language',
  MASTER = 'master',
}

export const topFiltersCountInitValues = Object.values(CoursesCategoryEnum).reduce(
  (acc, key) => {
    acc[key as CoursesCategoryEnum] = 0
    return acc
  },
  {} as Record<CoursesCategoryEnum, number>,
)
