export interface IContact {
  name: string
  email: string
  theme: string
  message: string
  is_agreed: boolean
}

export interface IContactResponse {
  id: number
  name: string
  email: string
  theme: string
  message: string
  is_agreed: boolean
  created_at: string
}
