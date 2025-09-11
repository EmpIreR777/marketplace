import type { IPriceRange, IRatingRange } from './coursesFilters/models'
import { RangeFilterEnum } from '@/enums/coursesFiltersEnum'

export interface IOption {
  id: number
  name: string
  translations?: string
}

export interface IBaseQueryParams {
  offset?: number
  limit?: number
  [key: string]: unknown
}

export interface IBaseResponse {
  count: number
  next: string | null
  previous: string | null
  results: []
}

export interface IBaseFilterCatalog {
  [key: string]: IOption[]
  [RangeFilterEnum.PRICE]?: IPriceRange
  [RangeFilterEnum.RATING]?: IRatingRange
}

export interface IUniversitiesFilterCatalog {
  [key: string]: IUniversityFilterItem
  [RangeFilterEnum]?: { min: number; max: number }
}

interface IUniversityFilterItem {
  items: IOption[]
  total: number
  total_search: number
}
