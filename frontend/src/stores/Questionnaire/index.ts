import { defineStore } from 'pinia'
import { getQuestions } from '@/api/questionnaire'
import type { IAanswersResult, IQuestionnaireStoreModel } from './model'
import type { IQuestion } from '@/api/questionnaire/models'
import type { IQuizQuestion } from '@/api/quiz/models'
// import { postStepBackQuizQuestion, resetQuizQuestions } from '@/api/quiz'

export const useQuestionnaireStore = defineStore('questionnaireStore', {
  state: (): IQuestionnaireStoreModel => ({
    questionnaireQuestions: null,
    currentQuestion: null,
    answersResults: null,
    questionnaireQuizQuestions: null,
    isLastQuestion: false,
  }),
  getters: {
    getQuestionnaireQuestions: (state) => state.questionnaireQuestions,
    getQuestionnaireQuizQuestions: (state) => state.questionnaireQuizQuestions,
    getAnswersResults: (state) => state.answersResults,
    getIsLastQuestion: (state) => state.isLastQuestion,
  },
  actions: {
    async loadQuestionnaireQuestions() {
      try {
        const response = await getQuestions()
        const questions = response.results
        this.setQuestionnaireQuestions(questions)
      } catch (error) {
        console.error('Get questions error:', error)
        throw error
      }
    },

    // async stepBackQuestionnaireQuizQuestion(data: IQuizQuestion) {
    //   try {
    //     await postStepBackQuizQuestion()
    //     this.setQuestionnaireQuizQuestionStepBack(data)
    //   } catch (error) {
    //     console.error('post step back error:', error)
    //     throw error
    //   }
    // },

    resetQuestionnaireQuizAnswersResults() {
      this.answersResults = null
    },

    setQuestionnaireQuestions(data: IQuestion[]) {
      this.questionnaireQuestions = data
    },

    setQuestionnaireQuizQuestion(data: IQuizQuestion) {
      this.questionnaireQuizQuestions = this.questionnaireQuizQuestions?.length
        ? Array.from(new Set([...this.questionnaireQuizQuestions, data]))
        : [data]
    },

    setQuestionnaireQuizQuestionStepBack(data: IQuizQuestion) {
      if (this.questionnaireQuizQuestions) {
        this.questionnaireQuizQuestions = this.questionnaireQuizQuestions.filter(
          ({ id }) => id !== data.id,
        )
      }
    },

    setStepBackAnswerResult(stepId: number) {
      if (this.answersResults?.[stepId]) {
        delete this.answersResults[stepId]
      }
    },

    setQuestionAnswerResults(data: IAanswersResult) {
      if (!this.answersResults) {
        this.answersResults = {}
      }

      if (this.answersResults && !this.answersResults?.[data.stepId]) {
        this.answersResults[data.stepId] = [...data.answers]
      }
    },

    setIsLastQuestion(data: boolean) {
      this.isLastQuestion = data
    },
  },
})
