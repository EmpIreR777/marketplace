import { useFieldRules } from '@/composable/useFieldRules'

const fieldRules = useFieldRules()

export const ATRIBUTES_FIZ = {
  fio: {
    type: 'STRING',
    name: 'ФИО:',
    validation: [fieldRules.isOnlyLetters],
  },
  fio_short: {
    type: 'STRING',
    name: 'ФИО сокращенно:',
    validation: [fieldRules.isOnlyLetters],
  },
  passport_serial: {
    type: 'STRING',
    name: 'Серия паспорта:',
    validation: [],
  },
  passport_number: {
    type: 'STRING',
    name: 'Номер паспорта:',
    validation: [],
  },
  passport_date: {
    type: 'DATE',
    name: 'Дата выдачи паспорта:',
    validation: [],
  },
  passport_issued_by: {
    type: 'STRING',
    name: 'Кем выдан паспорт:',
    validation: [],
  },
  passport_code_department: {
    type: 'STRING',
    name: 'Код подразделения:',
    validation: [],
  },
  inn: {
    type: 'STRING',
    name: 'ИНН:',
    validation: [],
  },
  contact_number: {
    type: 'STRING',
    name: 'Контактный телефон:',
    validation: [fieldRules.isPhoneNumber],
  },
  email: {
    type: 'STRING',
    name: 'E-mail:',
    validation: [fieldRules.isEmail],
  },
  address: {
    type: 'STRING',
    name: 'Адрес:',
    validation: [],
  },
  snils: {
    type: 'STRING',
    name: 'Снилс:',
    validation: [],
  },
  bank_name: {
    type: 'STRING',
    name: 'Название банка:',
    validation: [],
  },
  bank_bik: {
    type: 'STRING',
    name: 'БИК',
    validation: [],
  },
  bank_ks: {
    type: 'STRING',
    name: 'К/С:',
    validation: [],
  },
  bank_rs: {
    type: 'STRING',
    name: 'Р/С:',
    validation: [],
  },
}

export const ATRIBUTES_FOP = {
  fio: {
    type: 'STRING',
    name: 'ФИО:',
    validation: [fieldRules.isOnlyLetters],
  },
  fio_short: {
    type: 'STRING',
    name: 'ФИО сокращенно:',
    validation: [fieldRules.isOnlyLetters],
  },
  reg_number: {
    type: 'STRING',
    name: 'Номер записи ЕГР:',
    validation: [],
  },
  reg_date: {
    type: 'DATE',
    name: 'Дата выдачи ЕГР:',
    validation: [],
  },
  address: {
    type: 'STRING',
    name: 'Адрес:',
    validation: [],
  },
  bank_bik: {
    type: 'STRING',
    name: 'БИК',
    validation: [],
  },
  bank_rs: {
    type: 'STRING',
    name: 'Р/С:',
    validation: [],
  },
  bank_ks: {
    type: 'STRING',
    name: 'К/С:',
    validation: [],
  },
  bank_name: {
    type: 'STRING',
    name: 'Название банка:',
    validation: [],
  },
  inn: {
    type: 'STRING',
    name: 'ИНН:',
    validation: [],
  },
  contact_number: {
    type: 'STRING',
    name: 'Контактный телефон:',
    validation: [fieldRules.isPhoneNumber],
  },
  ogrnip_number: {
    type: 'STRING',
    name: 'ОГРНИП: ',
    validation: [],
  },
  email: {
    type: 'STRING',
    name: 'E-mail:',
    validation: [fieldRules.isEmail],
  },
}

export const ATRIBUTES_LLC = {
  name: {
    type: 'STRING',
    name: 'Название организации:',
    validation: [],
  },
  name_short: {
    type: 'STRING',
    name: 'Название организации (краткое):',
    validation: [],
  },
  director_name: {
    type: 'STRING',
    name: 'ФИО директора:',
    validation: [fieldRules.isOnlyLetters],
  },
  director_short_name: {
    type: 'STRING',
    name: 'ФИО директора сокр.:',
    validation: [fieldRules.isOnlyLetters],
  },
  buhgaler_name: {
    type: 'STRING',
    name: 'ФИО Бухгалтера:',
    validation: [fieldRules.isOnlyLetters],
  },
  buhgaler_short_name: {
    type: 'STRING',
    name: 'ФИО Бухгалтера сокр.:',
    validation: [fieldRules.isOnlyLetters],
  },
  kpp: {
    type: 'STRING',
    name: 'КПП:',
    validation: [],
  },
  okpo: {
    type: 'STRING',
    name: 'ОКПО:',
    validation: [],
  },
  registration_date: {
    type: 'DATE',
    name: 'Дата регистрации:',
    validation: [],
  },
  oktmo: {
    type: 'STRING',
    name: 'ОКТМО:',
    validation: [],
  },
  ogrn: {
    type: 'STRING',
    name: 'ОГРН:',
    validation: [],
  },
  inn: {
    type: 'STRING',
    name: 'ИНН:',
    validation: [],
  },
  bank_rs: {
    type: 'STRING',
    name: 'Р/С:',
    validation: [],
  },
  bank_ks: {
    type: 'STRING',
    name: 'К/С:',
    validation: [],
  },
  bank_name: {
    type: 'STRING',
    name: 'Название банка:',
    validation: [],
  },
  bank_bik: {
    type: 'STRING',
    name: 'БИК',
    validation: [],
  },
  contact_number: {
    type: 'STRING',
    name: 'Контактный телефон:',
    validation: [fieldRules.isPhoneNumber],
  },
  email: {
    type: 'STRING',
    name: 'E-mail:',
    validation: [fieldRules.isEmail],
  },
  address: {
    type: 'STRING',
    name: 'Адрес:',
    validation: [],
  },
}
