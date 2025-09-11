export enum MainStatistic {
  COURSES = 'courses',
  STUDENTS = 'students',
  AUTHORS = 'authors',
  SALES = 'sales',
  VUZ = 'vuz',
}
export const MainStatisticTitle = {
  [MainStatistic.COURSES]: 'Курсов',
  [MainStatistic.STUDENTS]: 'Студентов',
  [MainStatistic.AUTHORS]: 'Школ',
  [MainStatistic.SALES]: 'Сертификатов',
  [MainStatistic.VUZ]: 'ВУЗов',
} as const
