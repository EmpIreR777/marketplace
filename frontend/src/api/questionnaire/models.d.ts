export interface IAnswer {
  id: number
  text: string
}

export interface IQuestion {
  id: number
  text: string
  answers: IAnswer[]
}

export interface IGetQuestionnaireResponse {
  count: number
  next: string | null
  previous: string | null
  results: IQuestion[]
}
