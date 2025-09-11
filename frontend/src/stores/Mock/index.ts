import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import {
  onlineSchoolIcon,
  offlineSchoolIcon,
  universitiesIcon,
  trainingsIcon,
  masterClassesIcon,
  languageCoursesIcon,
  coursesIcon,
} from '@/assets/icons/training-options'
import {
  coursePic1,
  coursePic2,
  coursePic3,
  coursePic4,
  coursePic5,
  coursePic6,
  coursePic7,
  coursePic8,
  coursePic9,
} from '@/assets/tempCousesPic'
import type { QuestionnaireItem, ReviewType } from '@/types'
import type { ICourseItem } from '@/api/courses/models'
import { CoursesCategoryEnum } from '@/enums/coursesFiltersEnum'

export type TrainingOptionType = {
  id: number
  title: string
  subtitle: string
  key: CoursesCategoryEnum
  icon: string
}

const dataQuestionnaire: QuestionnaireItem[] = [
  {
    id: 1,
    question: 'Какие занятия Вам нравятся больше всего?',
    options: [
      'Решать головоломки или анализировать данные.',
      'Создавать что-то новое (рисовать, писать, конструировать).',
      'Помогать людям, решать их проблемы.',
      'Работать руками (собирать, чинить, строить).',
      'Работать с природой или животными.',
    ],
    isEnd: false,
  },
  {
    id: 2,
    question: 'Что приносит Вам наибольшее удовлетворение?',
    options: [
      'Найти решение сложной задачи.',
      'Видеть, как твоя работа вдохновляет других.',
      'Помогать команде достигать целей.',
      'На открытом воздухе.',
      'Исследовать и изучать окружающий мир.',
    ],
    isEnd: false,
  },
  {
    id: 3,
    question: 'Как Вы предпочитаете работать?',
    options: [
      'Самостоятельно, в своем темпе.',
      'В небольшой творческой команде.',
      'С людьми, предоставляя поддержку.',
      'Создавать что-то материальное и практичное.',
      'С техникой или компьютерами.',
    ],
    isEnd: false,
  },
  {
    id: 4,
    question: 'Какие предметы в школе Вам нравились больше всего?',
    options: [
      'Математика или информатика.',
      'Литература или искусство.',
      'Биология или география.',
      'Технологии или физкультура.',
      'Технологии или физкультура.',
    ],
    isEnd: false,
  },
  {
    id: 5,
    question: '',
    options: [],
    isEnd: true,
  },
]

const topCourses: ICourseItem[] = [
  {
    id: '1',
    course_image: coursePic1,
    course_duration: 3400,
    startDate: 'Старт 19 января',
    name: 'UI/UX Дизайнер – Уровень Beginner',
    price: '89000',
  },
  {
    id: '2',
    course_image: coursePic2,
    course_duration: 180,
    startDate: '60 мин.',
    name: 'Мастер-класс “Поверь в себя”',
    price: '9000',
  },
  {
    id: '3',
    course_image: coursePic3,
    course_duration: 2400,
    startDate: 'Старт 23 января',
    name: 'UI/UX Дизайнер – Уровень Pro',
    price: '69000',
  },
  {
    id: '4',
    course_image: coursePic4,
    course_duration: 1630,
    startDate: 'Старт 03 февраля',
    name: 'FrontEnd Dev – Уровень Beginner',
    price: '79000',
  },
  {
    id: '5',
    course_image: coursePic5,
    course_duration: 1600,
    startDate: 'Старт 09 февраля',
    name: 'Project Management – Уровень Pro',
    price: '49000',
  },
  {
    id: '6',
    course_image: coursePic6,
    course_duration: 1080,
    startDate: 'Старт 13 февраля',
    name: 'English Intermediate – Уровень B1',
    price: '9000',
  },
]

const reviews: ReviewType[] = [
  {
    fullName: 'Фамилия Имейко',
    date: '19 января 2024 в 16:39',
    position: 'UI/UX Дизайнер – Уровень Beginner',
    rating: 4,
    text: 'Тут будет некий текст отзыва, который написал пользователь. Текст больше трёх строк мы скрываем, но позволяем...',
  },
  {
    fullName: 'Фамилия Имейко',
    date: '20 января 2024 в 16:39',
    position: 'UI/UX Дизайнер – Уровень Beginner',
    rating: 3,
    text: 'Тут будет некий текст отзыва, который написал пользователь. Текст больше трёх строк мы скрываем, но позволяем...',
  },
  {
    fullName: 'Фамилия Имейко',
    date: '21 января 2024 в 16:39',
    position: 'UI/UX Дизайнер – Уровень Beginner',
    rating: 5,
    text: 'Тут будет некий текст отзыва, который написал пользователь. Текст больше трёх строк мы скрываем, но позволяем...',
  },
  {
    fullName: 'Фамилия Имейко',
    date: '22 января 2024 в 16:39',
    position: 'UI/UX Дизайнер – Уровень Beginner',
    rating: 4,
    text: 'Тут будет некий текст отзыва, который написал пользователь. Текст больше трёх строк мы скрываем, но позволяем...',
  },
  {
    fullName: 'Фамилия Имейко',
    date: '23 января 2024 в 16:39',
    position: 'UI/UX Дизайнер – Уровень Beginner',
    rating: 5,
    text: 'Тут будет некий текст отзыва, который написал пользователь. Текст больше трёх строк мы скрываем, но позволяем...',
  },
]

const dataTrainingOptions: TrainingOptionType[] = [
  {
    id: 1,
    title: 'Школы',
    subtitle: '15 320',
    key: CoursesCategoryEnum.SCHOOL,
    icon: offlineSchoolIcon,
  },
  {
    id: 2,
    title: 'Онлайн курсы',
    subtitle: '8 732 ',
    key: CoursesCategoryEnum.ONLINE,
    icon: onlineSchoolIcon,
  },
  {
    id: 3,
    title: 'Оффлайн курсы',
    subtitle: '32 019',
    key: CoursesCategoryEnum.OFFLINE,
    icon: coursesIcon,
  },
  {
    id: 4,
    title: 'Тренинги',
    subtitle: '19 907',
    key: CoursesCategoryEnum.TRAINING,
    icon: trainingsIcon,
  },
  {
    id: 5,
    title: 'Языковые курсы',
    subtitle: '12 430',
    key: CoursesCategoryEnum.LANGUAGE,
    icon: languageCoursesIcon,
  },
  {
    id: 6,
    title: 'Мастер-классы',
    subtitle: '7 543',
    key: CoursesCategoryEnum.MASTER,
    icon: masterClassesIcon,
  },
]

const allCourses: ICourseItem[] = [
  {
    id: '1',
    course_image: coursePic1,
    course_duration: 3400,
    startDate: 'Старт 19 января',
    name: 'UI/UX Дизайнер – Уровень Beginner',
    price: '89000',
  },
  {
    id: '2',
    course_image: coursePic2,
    course_duration: 180,
    startDate: '60 мин.',
    name: 'Мастер-класс “Поверь в себя”',
    price: '9000',
  },
  {
    id: '3',
    course_image: coursePic3,
    course_duration: 2400,
    startDate: 'Старт 23 января',
    name: 'UI/UX Дизайнер – Уровень Pro',
    price: '69000',
  },
  {
    id: '4',
    course_image: coursePic4,
    course_duration: 1630,
    startDate: 'Старт 03 февраля',
    name: 'FrontEnd Dev – Уровень Beginner',
    price: '79000',
  },
  {
    id: '5',
    course_image: coursePic5,
    course_duration: 1600,
    startDate: 'Старт 09 февраля',
    name: 'Project Management – Уровень Pro',
    price: '49000',
  },
  {
    id: '6',
    course_image: coursePic6,
    course_duration: 1080,
    startDate: 'Старт 13 февраля',
    name: 'English Intermediate – Уровень B1',
    price: '9000',
  },
  {
    id: '7',
    course_image: coursePic7,
    course_duration: 900,
    startDate: 'Старт 16 февраля',
    name: 'Программирование Java – Детский',
    price: '19000',
  },
  {
    id: '8',
    course_image: coursePic8,
    course_duration: 3600,
    startDate: 'Старт 26 февраля',
    name: 'Marketing – Start',
    price: '49000',
  },
  {
    id: '9',
    course_image: coursePic9,
    course_duration: 600,
    startDate: 'Старт 1 марта',
    name: '3D моделирование – Start',
    price: '39000',
  },
]

const courseTabs = [
  {
    id: 1,
    name: 'О курсе',
    value: 'about_course',
  },
  {
    id: 2,
    name: 'Оплата',
    value: 'payment',
  },
  {
    id: 3,
    name: 'Отзывы',
    value: 'reviews',
  },
  {
    id: 4,
    name: 'Частые Вопросы',
    value: 'FAQ',
  },
  {
    id: 5,
    name: 'Автор',
    value: 'author',
  },
]

const aboutCourseTabContent = `
    <section>
      <h1>О чём этот курс?</h1>
      <div>
        <h2 >Чему вы научитесь</h2>
        <ul>
          <li>Создавать веб-приложения с нуля</li>
          <li>Работать с современными фреймворками</li>
          <li>Улучшать пользовательский интерфейс</li>
          <li>Оптимизировать производительность кода</li>
          <li>Разрабатывать адаптивный дизайн</li>
          <li>Эффективно работать в команде</li>
        </ul>
      </div>
      <div>
        <h2 class="qwerty">Описание курса</h2>
        <p>
          Узнайте, как создавать проекты с нуля, улучшать свои навыки и работать с современными инструментами.
          Этот курс поможет вам освоить новые подходы и добиться большего в вашей профессии.
        </p>
        <p>
          Вы научитесь разрабатывать решения, которые соответствуют современным стандартам. Узнаете, как
          эффективно применять полученные знания на практике, улучшите свои технические и аналитические способности,
          а также разберетесь в тонкостях работы с командой. Курс подходит как для начинающих, так и для тех,
          кто хочет обновить свои знания.
        </p>
      </div>
    </section>
  `

const paymentTabContent = `<section>
      <h1>Способы оплаты и расчёт</h1>
      <div>
        <p>Aspernatur rerum omnis est unde. Autem a non labore numquam tempore. Voluptatibus ea quod ut ipsa sunt
          adipisci
          non enim rerum. Voluptas consequatur voluptatibus quod sed ullam explicabo quia. Ipsam dicta amet. Laudantium
          commodi quia consequatur.</p>
        <p> Интеграция с популярными платежными системами (СБП, Сбер pay, T pay, банковские карты)</p>
        <ul>
          <li>Система генерации счетов и квитанций.</li>
          <li>Защищенная передача данных для обеспечения безопасности платежей (SSL, PCI DSS).</li>
          <li>Покупка курсов через мобильную и браузерную версию.</li>
          <li>Поддержка скидок, промокодов и купонов.</li>
        </ul>
      </div>
    </section>`

const courseReviewItemsContent = [
  {
    id: 1,
    userAvatar: 'https://randomuser.me/api/portraits/men/1.jpg',
    userName: 'Имя Фамилия',
    rating: 4,
    reviewText:
      'Проходила курс по веб-дизайну, и это было невероятно полезно! Материал подается доступно, даже для' +
      ' новичков. Понравилось, что много практики — уже в процессе обучения я смогла создать свой первый проект. ',
    time: '2 нед. назад',
  },
  {
    id: 2,
    userAvatar: 'https://randomuser.me/api/portraits/men/2.jpg',
    userName: 'Имя Фамилия',
    rating: 5,
    reviewText:
      'Прошел курс по управлению проектами. Это настоящая находка! Четкая структура уроков, множество кейсов' +
      ' из реальной жизни и практические задания помогли мне понять, как эффективно вести проекты. ',
    time: '2 нед. назад',
  },
  {
    id: 3,
    userAvatar: 'https://randomuser.me/api/portraits/men/3.jpg',
    userName: 'Имя Фамилия',
    rating: 4,
    reviewText:
      'Брал курс , чтобы подтянуть навыки для новой работы. Очень круто, что в курсе были реальные задачи,' +
      ' которые я мог сразу применить в проектах. Преподаватели классные, объясняют всё просто и понятно. Однозначно' +
      ' буду проходить у них еще курсы!',
    time: '2 нед. назад',
  },
  {
    id: 4,
    userAvatar: 'https://randomuser.me/api/portraits/men/4.jpg',
    userName: 'Имя Фамилия',
    rating: 5,
    reviewText:
      'Курс превзошел мои ожидания! Все техники, которые изучила, уже применяю на работе и в личной жизни.' +
      ' Формат подачи материала удобный, можно проходить в своем темпе. Отдельное спасибо за чек-листы и дополнительные' +
      ' материалы!',
    time: '2 нед. назад',
  },
  {
    id: 5,
    userAvatar: 'https://randomuser.me/api/portraits/men/5.jpg',
    userName: 'Имя Фамилия',
    rating: 4,
    reviewText:
      'Это был мой первый онлайн-курс, и я не ожидала, что он будет таким интересным и полезным. Особенно' +
      ' понравилась подача материала: короткие видео, практические задания и живые вебинары.',
    time: '2 нед. назад',
  },
  {
    id: 6,
    userAvatar: 'https://randomuser.me/api/portraits/men/6.jpg',
    userName: 'Имя Фамилия',
    rating: 5,
    reviewText:
      'Курс действительно хороший, но есть небольшие недочеты. Понравилось, что материал изложен доступно,' +
      ' много примеров и практики. Однако иногда не хватало глубины в некоторых темах — хотелось бы более детального' +
      ' разбора. В остальном всё супер!',
    time: '2 нед. назад',
  },
]

const courseQuestinsContent = [
  {
    id: 1,
    question: 'В: Здесь часто задаваемый вопрос?',
    answer: 'О: Здесь ответ на вопрос выше',
  },
  {
    id: 2,
    question: 'В: Здесь часто задаваемый вопрос?',
    answer: 'О: Здесь ответ на вопрос выше',
  },
  {
    id: 3,
    question: 'В: Здесь часто задаваемый вопрос?',
    answer: 'О: Здесь ответ на вопрос выше',
  },
  {
    id: 4,
    question: 'В: Здесь часто задаваемый вопрос?',
    answer: 'О: Здесь ответ на вопрос выше',
  },
  {
    id: 5,
    question: 'В: Здесь часто задаваемый вопрос?',
    answer: 'О: Здесь ответ на вопрос выше',
  },
]

export const useMockCoursesStore = defineStore('coursesMockStore', () => {
  // Состояние

  const questionnaire = ref<QuestionnaireItem[]>(dataQuestionnaire)
  const topCoursesMain = ref<ICourseItem[]>(topCourses)

  const currentReviews = ref<ReviewType[]>(reviews)
  const trainingOptions = ref<TrainingOptionType[]>(dataTrainingOptions)
  const allCoursesMain = ref<ICourseItem[]>(allCourses)
  const tabsCoursePage = ref(courseTabs)
  const contentAboutCourseTab = ref(aboutCourseTabContent)
  const contentPaymentTab = ref(paymentTabContent)
  const contentCourseReviewItems = ref(courseReviewItemsContent)
  const contentCourseQuestions = ref(courseQuestinsContent)

  // Геттеры
  const getQuestionnaire = computed(() => questionnaire.value)
  const getTopCourses = computed(() => topCoursesMain.value)
  const getCurrentReviews = computed(() => currentReviews.value)

  const getAllTrainingOptions = computed(() => trainingOptions.value)
  const getAllCourses = computed(() => allCoursesMain.value)
  const getTabsCoursePage = computed(() => tabsCoursePage.value)
  const getContentAboutCourseTab = computed(() => contentAboutCourseTab.value)
  const getContentPaymentTab = computed(() => contentPaymentTab.value)
  const getContentCourseReviewItems = computed(() => contentCourseReviewItems.value)
  const getContentCourseQuestions = computed(() => contentCourseQuestions.value)

  return {
    questionnaire,
    topCoursesMain,
    currentReviews,
    trainingOptions,
    allCourses,
    tabsCoursePage,
    contentAboutCourseTab,
    contentPaymentTab,
    contentCourseReviewItems,
    contentCourseQuestions,

    getQuestionnaire,
    getTopCourses,
    getCurrentReviews,
    getAllTrainingOptions,
    getAllCourses,
    getTabsCoursePage,
    getContentAboutCourseTab,
    getContentPaymentTab,
    getContentCourseReviewItems,
    getContentCourseQuestions,
  }
})
