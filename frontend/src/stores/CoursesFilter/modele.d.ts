import type { IFilterProperties } from '@/api/coursesFilters/models'

export type SelectedFilters = Record<string, string[] | number[] | string | number>

export interface ICoursesStoreModel {
  coursesFilters: IFilterProperties | null
  selectedFilters: SelectedFilters | null
}
