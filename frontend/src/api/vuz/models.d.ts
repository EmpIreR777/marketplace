import type { IBaseQueryParams, IBaseResponse } from '@/api/models'
import type { IAuthor } from '@/api/author/models'
import type { PaginationParams } from '@/types/index'

export interface IUniversitiesQueryParams extends PaginationParams {
  name?: string
  city?: string
  subject?: string
  metro?: string
  min_rating?: string
  max_rating?: string
  min_cost?: string
  max_cost?: string
  has_hostel?: string
  is_state?: string
  is_military?: string
  ordering?: string
}

export interface IUniversityOrgranizationListResponse {
  count: number
  next: string | null
  previous: string | null
  results: IUniversityOrgranization[]
}

export interface IUniversityProgramResponse {
  count: number
  next: string | null
  previous: string | null
  results: IUniversityProgram[]
}

export interface IUniversityOrgranization {
  id: number
  type: string
  source: string
  name: string
  code?: string | null
  full_name?: string | null
  short_name?: string | null
  obrnadzor_name?: string | null
  obrnadzor_checked?: boolean | null
  short_seo?: string | null
  about?: string | null
  logo?: string | null
  logo_storage?: string | null
  video_link?: string | null
  sort?: number | null
  sort_for_region?: number | null
  sort_for_top?: number | null
  published: boolean
  is_state: boolean
  is_hostel: boolean
  is_military: boolean
  is_departmental: boolean
  is_partner: boolean
  has_leads: boolean
  is_confirmed: boolean
  is_top100: boolean
  inn?: string | null
  kpp?: string | null
  monitoring_code?: string | null
  longitude_latitude?: string | null
  organization_type?: string | null
  sub_type?: string | null
  site?: string | null
  licence_num?: string | null
  licence_date?: string | null
  accreditation_number?: string | null
  accreditation_date?: string | null
  rating?: number | null
  esi?: number | null
  esi24?: string | null
  esi_marks?: number | null
  ege_score?: string | null
  cost?: number | null
  old_names?: string | null
  delete_reason?: string | null
  confirmed_and_date?: string | null
  calculation_data: ICalculationData | null
  created_at: string
  updated_at: string
  external_updated_at?: string | null
  city: ICity | null
  contact: IContact
  metro: IMetro
  subject: ISubject
  admission_office: IAdmissionOffice
  programs_count: number
}

export interface IUniversityProgram {
  id: number
  profile?: string | null
  duration?: number | null
  budget_places?: number | null
  budget_score?: number | null
  commercial_places?: number | null
  commercial_score?: number | null
  cost?: number | null
  faculty: IFaculty
  specialty: ISpecialty
  form: IForm
  organization_vuz: number
  calculation_data: IProgramCalculationData | null
}

interface IProgramCalculationData {
  exams: string
  exams_name: string
  full_exams: string
  is_favorite: boolean
}

export interface IUniversityFilterParams extends PaginationParams {
  name?: string
  search?: string
  city?: number
  subject?: number
  metro?: number
  faculty?: number
  specialty?: number
  form?: number
  min_rating?: number
  max_rating?: number
  min_cost?: number
  max_cost?: number
  has_hostel?: boolean
  is_state?: boolean
  is_military?: boolean
  filter_type?: string
}

interface ICity {
  id: number
  name: string
  name_rp?: string | null
  is_capital: boolean
  city_type?: string | null
}

interface IContact {
  site?: string | null
  phones?: string | null
  email?: string | null
  address?: string | null
  post_index?: string | null
}

interface IMetro {
  id: number
  name: string
}

interface ISubject {
  id: number
  name?: string | null
  name_rp?: string | null
}

interface IAdmissionOffice {
  type: string
  source: string
  site?: string | null
  email?: string | null
  phones?: Record<string, any> | null
  address?: string | null
  longitude_latitude?: string | null
  post_index?: string | null
  schedule?: Record<string, any> | null
  description?: string | null
  start_date?: string | null
  end_date?: string | null
  is_full_year: boolean
}

interface ICalculationData {
  att: number | null
  avg_score: number
  budget_places: number
  budget_score: number
  canceled_score_count: number
  city_id: number
  city_name: string
  commercial_places: number
  commercial_score: number
  cost: number
  cost_min: number
  explode: boolean
  faculty_count: number
  license_specialties_count: number
  monitorings: IMonitoring
  negative_score_count: number
  neutral_score_count: number
  not_implement_specialties_count: number
  percent_of_hyped_reviews: number
  positive_score_count: number
  reviews_count: number
  specialties_count: number
  subject_id: number
  subject_name: string
  top10: boolean
  top500: boolean
}

interface IMonitoring {
  att: number
  pay_avg: number
  free_avg: number
}
interface IFaculty {
  id: number
  name: string
  address?: string | null
  email?: string | null
  phone?: string | null
}

interface ISpecialty {
  id: number
  name: string
  code?: string | null
  qualification?: string | null
  description?: string | null
  level_code: string | null
}

interface IForm {
  id: number
  name: string
}

export interface IUniversityProgramFilterParams {
  name?: string
  faculty?: number
  specialty?: number
  form?: number
  min_budget_places?: number
  max_budget_places?: number
  min_budget_score?: number
  max_budget_score?: number
  min_commercial_places?: number
  max_commercial_places?: number
  min_commercial_score?: number
  max_commercial_score?: number
  min_cost?: number
  max_cost?: number
  min_duration?: number
  max_duration?: number
}
