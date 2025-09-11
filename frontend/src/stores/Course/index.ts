import { defineStore } from 'pinia'
import type { ICourseStoreModel, IPartialEditorCourse } from '@/stores/Course/models'
import { getCourseById, patchCourse, postCourse } from '@/api/courses'
import type { ICourseDetail, IEditorCourse } from '@/api/courses/models'
import type { IFilterProperties } from '@/api/coursesFilters/models'
import { getCoursesFilters } from '@/api/coursesFilters'
import { useRouter } from 'vue-router'
import { useFormData } from '@/composable/useFormData'
import { useChangedFields } from '@/composable/useChangedFields'
import { getFeedbacks } from '@/api/feedbacks'
import type { IFeedbacksParams } from '@/api/feedbacks/models'

export const useCourseStore = defineStore('courseStore', {
  state: (): ICourseStoreModel => {
    return {
      course: null,
      originCourse: null,
      isLoading: false,
      filtersCatalog: null,
      router: useRouter(),
      feedbacks: [],
      isReportDialog: false,
      isRefundDialog: false,
    }
  },

  getters: {},

  actions: {
    setIsReportDialog(val: boolean) {
      this.isReportDialog = val
    },

    setIsRefundDialog(val: boolean) {
      this.isRefundDialog = val
    },

    async loadFeedbacks() {
      const params: IFeedbacksParams = {
        feedback_to_course: this.course?.id,
        limit: 10,
        offset: 0,
      }
      const { results } = await getFeedbacks(params)
      this.feedbacks = results
    },
    setIsloading(val: boolean) {
      this.isLoading = val
    },

    setCourse(data: ICourseDetail | null) {
      this.course = data
    },

    setOriginCourse(data: ICourseDetail) {
      this.originCourse = data
    },

    setFiltersCatalog(data: IFilterProperties | null) {
      this.filtersCatalog = data
    },

    async loadCourseById(id: string) {
      try {
        this.isLoading = true
        this.setCourse(null)
        const response = await getCourseById(id)
        this.setCourse(response)
        this.setOriginCourse(response)
        return response
      } catch (error) {
        return Promise.reject(error)
      } finally {
        this.isLoading = false
      }
    },

    async createCourse(data: IEditorCourse) {
      const formData = useFormData(data)

      try {
        return await postCourse(formData)
      } catch (error) {
        console.error('Ошибка создания объекта:', error)
        return Promise.reject(error)
      }
    },

    async updateCourse(id: string, data: IPartialEditorCourse) {
      if (!id) return

      const changedFields = this.originCourse ? useChangedFields(this.originCourse, data) : data

      if (Object.keys(changedFields).length === 0) return

      const formData = useFormData(changedFields)

      try {
        const response = await patchCourse(id, formData)
        this.setCourse(response.data)
        this.setOriginCourse(response.data)
        return response.data
      } catch (error) {
        console.error('Ошибка обновления объекта:', error)
        return Promise.reject(error)
      }
    },

    async loadFiltersCatalog() {
      if (!this.filtersCatalog) {
        try {
          const response = await getCoursesFilters()
          this.setFiltersCatalog(response)
          return response
        } catch (error) {
          console.error('Ошибка зкгрузки фильтров:', error)
          return Promise.reject(error)
        }
      }

      return Promise.resolve(this.filtersCatalog)
    },

    clearCourse() {
      this.course = null
      this.originCourse = null
    },

    clearStore() {
      this.clearCourse()
      this.filtersCatalog = null
    },
  },
})
