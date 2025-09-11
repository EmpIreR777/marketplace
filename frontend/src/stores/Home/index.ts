import { defineStore } from 'pinia'
import { getCourses } from '@/api/courses'
import type { ICourseItem, ICoursesQueryParams } from '@/api/courses/models'
import { getFeedbacks } from '@/api/feedbacks'
import type { IFeedback, IFeedbacksParams } from '@/api/feedbacks/models'
import type { IHomeStoreModel } from '@/stores/Home/models'
import type { IMainPageStatistic } from '@/api/main-page-statistic/models'
import { getMainPageStatistic } from '@/api/main-page-statistic'
import { MainStatistic, MainStatisticTitle } from '@/enums/mainStatisticEnum'
import { usePluralize } from '@/composable/usePluralize'

const { pluralize, getPluralForms } = usePluralize()

export const useHomeStore = defineStore('homeStore', {
  state: (): IHomeStoreModel => {
    return {
      courses: [],
      feedbacks: [],
      statistic: null,
    }
  },

  getters: {
    getCoursesList(state) {
      return state.courses
    },
    getStatistic(state) {
      if (!state.statistic) return []
      return Object.entries(state.statistic)
        .filter(([key]) => key !== MainStatistic.SALES)
        .map(([key, value]) => {
          return {
            key: pluralize(value, getPluralForms(MainStatisticTitle[key as MainStatistic])),
            value,
          }
        })
    },
  },

  actions: {
    async initHomeStore() {
      const paramsCourses = {
        offset: 0,
        limit: 20,
        is_top_sale: true,
      }
      const paramsFeedbacks = {
        offset: 0,
        limit: 20,
      }
      await this.loadStatistic()
      await this.loadTopCoursesList(paramsCourses)
      await this.loadFeedbacksList(paramsFeedbacks)
    },
    async loadTopCoursesList(params?: ICoursesQueryParams) {
      const response = await getCourses(params)
      this.setCoursesList(response.results)
    },
    async loadFeedbacksList(params?: IFeedbacksParams) {
      const response = await getFeedbacks(params)
      this.setFeedbacksList(response.results)
    },
    async loadStatistic() {
      const response = await getMainPageStatistic()
      this.setStatistic(response)
    },
    setCoursesList(data: ICourseItem[]) {
      this.courses = data
    },
    setFeedbacksList(data: IFeedback[]) {
      this.feedbacks = data
    },
    setStatistic(data: IMainPageStatistic) {
      this.statistic = data
    },

    clearStore() {
      this.setCoursesList([])
      this.setFeedbacksList([])
    },
  },
})
