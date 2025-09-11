import { api } from '@/utils/axios'
import type { IContact, IContactResponse } from './models'

export enum Api {
  CONTACTS = '/api/contacts/',
}

export async function postContactForm(body: IContact) {
  try {
    const { data, status } = await api.post<IContactResponse>(Api.CONTACTS, body)
    return { data, status }
  } catch (error) {
    console.error('Post contact form error:', error)
    throw error
  }
}
