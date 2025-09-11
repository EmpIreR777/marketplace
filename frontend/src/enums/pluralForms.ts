import { MainStatistic, MainStatisticTitle } from '@/enums/mainStatisticEnum'

export const PluralForms = {
  [MainStatisticTitle[MainStatistic.COURSES]]: ['Курс', 'Курса', 'Курсов'],
  [MainStatisticTitle[MainStatistic.STUDENTS]]: ['Студент', 'Студента', 'Студентов'],
  [MainStatisticTitle[MainStatistic.AUTHORS]]: ['Школа', 'Школы', 'Школ'],
  [MainStatisticTitle[MainStatistic.SALES]]: ['Сертификат', 'Сертификата', 'Сертификатов'],
  [MainStatisticTitle[MainStatistic.VUZ]]: ['ВУЗ', 'ВУЗа', 'ВУЗов'],
} as const
