import { defineStore } from 'pinia'
import { getCoursesFilters } from '@/api/coursesFilters'
import type { IFilterProperties } from '@/api/coursesFilters/models'
import type { ICoursesStoreModel, SelectedFilters } from './modele'

export const useCoursesFilterStore = defineStore('coursesFilter', {
  state: (): ICoursesStoreModel => ({
    coursesFilters: null,
    selectedFilters: null,
  }),

  actions: {
    async loadCoursesFilters() {
      try {
        // Get params from selectedFilters for API
        const params = Object.keys(this.selectedFilters ?? {}).reduce(
          (acc: Record<string, string>, key) => {
            const value = this.selectedFilters?.[key]
            if (value === undefined) return acc

            acc[key] = Array.isArray(value) ? (value as string[]).join(',') : String(value)
            return acc
          },
          {},
        )
        const response = await getCoursesFilters(params)

        // Keep showing filters when there are no filters
        const isEmptyFilters = Object.values(response).every((key) => !key.length)
        if (isEmptyFilters) return

        this.setCoursesFilters(response)

        return response
      } catch (error) {
        // TODO notify: show error message
        return Promise.reject(error)
      }
    },
    setCoursesFilters(data: IFilterProperties) {
      this.coursesFilters = data
    },
    setSelectedFilters(data: SelectedFilters) {
      if (this.selectedFilters === null) {
        this.selectedFilters = {}
      }
      const value = Object.values(data)

      if ((typeof value[0] === 'string' || Array.isArray(value[0])) && value[0].length === 0) {
        const key = Object.keys(data)[0]

        delete this.selectedFilters[key]
      } else {
        this.selectedFilters = { ...this.selectedFilters, ...data }
      }
    },
    clearSelectedCheckboxFilters() {
      if (this.coursesFilters && this.selectedFilters) {
        const coursesFiltersKeys = Object.keys(this.coursesFilters)
        const selectedFiltersKeys = Object.keys(this.selectedFilters)

        selectedFiltersKeys.forEach((key) => {
          if (coursesFiltersKeys.includes(key) && this.selectedFilters?.[key]) {
            delete this.selectedFilters[key]
          }
        })
      }
    },
    clearSelectedFilters() {
      this.selectedFilters = null
    },
  },

  getters: {
    getCoursesFilters(state) {
      return state.coursesFilters
    },
    getSelectedFilters(state) {
      return state.selectedFilters
    },
    getActiveFiltersCount(state) {
      return Object.values(state.selectedFilters ?? {}).reduce((count, value) => {
        if (Array.isArray(value)) {
          return count + value.length
        } else if (value !== null && value !== undefined && value !== '') {
          return count + 1
        }
        return count
      }, 0)
    },
  },
})
