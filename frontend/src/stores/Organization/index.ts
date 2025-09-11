import { defineStore } from 'pinia'
import type { IOrganizationStoreModel } from './models'
import type { IOrganizationBase } from '@/api/organizations/models'
import { getOrganizationById } from '@/api/organizations'

export const useOrganizationStore = defineStore('organizationStore', {
  state: (): IOrganizationStoreModel => {
    return {
      course: null,
      isLoading: false,
    }
  },

  getters: {
    getOrganization(state) {
      return state.course
    },
  },

  actions: {
    async loadOrganizationById(id: string) {
      try {
        const response = await getOrganizationById(id)
        this.setOrganization(response)
        return response
      } catch (error) {
        return Promise.reject(error)
      }
    },

    setOrganization(data: IOrganizationBase) {
      this.course = data
    },
  },
})
