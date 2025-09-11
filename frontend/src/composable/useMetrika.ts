import { useYandexMetrika } from 'yandex-metrika-vue3'

interface MetrikaComposition {
  contactFormSubmit: () => void
  jivoDialogStart: () => void
  studentRegistration: () => void
  studentUpdate: () => void
  authorRegistration: () => void
  authorUpdate: () => void
  authorReview: (id: number) => void
  coursePurchase: (id: string) => void
  coursePayment: (id: string) => void
  courseReview: (id: string) => void
  courseCreate: () => void
  changeCourseFilter: () => void
}

enum MetrikaEventEnum {
  CONTACT_FORM_SUBMIT = 'contact-form',
  JIVO_DIALOG_START = 'jivo-start',
  STUDENT_REGISTRATION = 'register-student',
  STUDENT_UPDATE = 'fill-student',
  AUTHOR_REGISTRATION = 'register-teacher',
  AUTHOR_UPDATE = 'fill-teacher',
  AUTHOR_REVIEW = 'review-teacher', // ${ID}
  COURSE_PURCHASE = 'buy-course', // ${ID}
  COURSE_PAYMENT = 'pay-course', // ${ID}
  COURSE_REVIEW = 'review-course', // ${ID}
  COURSE_CREATE = 'add-course',
  CHANGE_FILTER = 'change-filter-courses',
}

export function useMetrika(): MetrikaComposition {
  const yandexMetrika = useYandexMetrika()

  const contactFormSubmit = (): void => {
    yandexMetrika.reachGoal(MetrikaEventEnum.CONTACT_FORM_SUBMIT)
  }

  const jivoDialogStart = (): void => {
    yandexMetrika.reachGoal(MetrikaEventEnum.JIVO_DIALOG_START)
  }

  const studentRegistration = (): void => {
    yandexMetrika.reachGoal(MetrikaEventEnum.STUDENT_REGISTRATION)
  }

  const studentUpdate = (): void => {
    yandexMetrika.reachGoal(MetrikaEventEnum.STUDENT_UPDATE)
  }

  const authorRegistration = (): void => {
    yandexMetrika.reachGoal(MetrikaEventEnum.AUTHOR_REGISTRATION)
  }

  const authorUpdate = (): void => {
    yandexMetrika.reachGoal(MetrikaEventEnum.AUTHOR_UPDATE)
  }

  const authorReview = (id: number): void => {
    yandexMetrika.reachGoal(`${MetrikaEventEnum.AUTHOR_REVIEW}-${id}`)
  }

  const coursePurchase = (id: string): void => {
    yandexMetrika.reachGoal(`${MetrikaEventEnum.COURSE_PURCHASE}-${id}`)
  }

  const coursePayment = (id: string): void => {
    yandexMetrika.reachGoal(`${MetrikaEventEnum.COURSE_PAYMENT}-${id}`)
  }

  const courseReview = (id: string): void => {
    yandexMetrika.reachGoal(`${MetrikaEventEnum.COURSE_REVIEW}-${id}`)
  }

  const courseCreate = (): void => {
    yandexMetrika.reachGoal(MetrikaEventEnum.COURSE_CREATE)
  }
  const changeCourseFilter = (): void => {
    yandexMetrika.reachGoal(MetrikaEventEnum.CHANGE_FILTER)
  }

  return {
    contactFormSubmit,
    jivoDialogStart,
    studentRegistration,
    studentUpdate,
    authorRegistration,
    authorUpdate,
    authorReview,
    coursePurchase,
    coursePayment,
    courseReview,
    courseCreate,
    changeCourseFilter,
  }
}
