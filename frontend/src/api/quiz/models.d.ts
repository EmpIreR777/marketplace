export interface IQuizAnswer {
  id: number
  text: string
  answer_category: string
  openness_priority: string
}

// GET

export interface IQuizQuestion {
  id: number
  title: string
  text: string
  has_multiple_answers: boolean
  answers: IQuizAnswer[]
}

// POST

export interface ISelectedAnswersBody {
  quiz: {
    [key: string]: number[]
  }
}

export interface ISavedAnswersResponse {
  url: string
}

// DELETE

export interface IDeleteAnswersResponse {
  detail: string
}

// POST
// /quiz/back/

// res
export interface IStepBackAnswersResponse {
  detail: string
  current_state: string
}
