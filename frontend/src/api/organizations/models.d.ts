// export interface IOrganizationBase {
//   alias: string | null
//   status: string
//   name: string | null
//   full_name: string | null
//   prepositional_name: string | null
//   genitive_name: string | null
//   description: string | null
//   type: string | null
//   logo: string | null
//   round_logo: string | null
//   square_logo: string | null
//   is_school: boolean
//   partner_card: boolean
//   license: string | null
//   phone: string | null
//   email: string | null
//   website: string | null
//   address: string | null
//   legal_address: string | null
//   personal_account_name: string | null
//   personal_account_site: string | null
//   leadership: string | null
//   bik: string | null
//   inn: string | null
//   kpp: string | null
//   ogrn: string | null
//   complex_calculated_rating_value: number | null
//   reviews_count: number | null
//   education_type: string | null
//   graduates: number | null
//   is_premium_partner: boolean
//   learning_types: Array<object>
// }

export interface IOrganizationBase{
  id: string;
  alias?: string;
  status: string;
  name?: string;
  full_name?: string;
  prepositional_name?: string;
  genitive_name?: string;
  description?: string;
  type?: string;
  logo?: string;
  round_logo?: string;
  square_logo?: string;
  is_school: boolean;
  partner_card: boolean;
  license?: string;
  phone?: string;
  email?: string;
  website?: string;
  address?: string;
  legal_address?: string;
  personal_account_name?: string;
  personal_account_site?: string;
  leadership?: string;
  bik?: string;
  inn?: string;
  kpp?: string;
  ogrn?: string;
  complex_calculated_rating_value?: number;
  reviews_count?: number;
  education_type?: string;
  graduates?: number;
  is_premium_partner: boolean;
  learning_types?: number[];
}

