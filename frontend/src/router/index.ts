import { createRouter, createWebHistory } from 'vue-router'
// import { useUser } from '@/stores/User'
import UniversitiesPage from '@/views/UniversitiesPage.vue'
import UniversityDetailPage from '@/views/university-detail/index.vue'
import Account from '@/views/account/index.vue'
import Notifications from '@/views/account/notifications/index.vue'
import Statistics from '@/views/account/statistics/index.vue'
import Calendar from '@/views/account/calendar/index.vue'
import MyCourses from '@/views/account/my-courses/index.vue'
import Profile from '@/views/account/profile/index.vue'
import PaymentHistory from '@/views/account/payment-history/index.vue'
import PurchasedCourses from '@/views/account/purchased-courses/index.vue'
import Tariff from '@/views/account/tariff/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      props: { showFooter: true },
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomePage.vue'),
        },
        {
          path: 'courses',
          name: 'Courses',
          component: () => import('@/views/CoursesPage.vue'),
        },
        {
          path: '/course/:id',
          name: 'CourseDetail',
          component: () => import('@/views/CoursePage.vue'),
          props: true,
        },
        {
          path: 'universities',
          name: 'universities',
          component: UniversitiesPage,
        },
        {
          path: '/universities/:id',
          redirect: (to) => `/universities/${to.params.id}/programs`,
        },
        {
          path: '/universities/:id/:tab',
          name: 'university-detail',
          component: UniversityDetailPage,
          props: true,
          beforeEnter: (to, _, next) => {
            const allowedTabs = ['programs', 'about', 'payment', 'reviews', 'faq']
            if (allowedTabs.includes(to.params.tab as string)) {
              next()
            } else {
              next(`/universities/${to.params.id}/programs`)
            }
          },
        },
        {
          path: 'contacts',
          name: 'Contacts',
          component: () => import('@/views/ContactsPage.vue'),
        },
        {
          path: 'reviews',
          name: 'Reviews',
          component: () => import('@/views/ReviewsPage.vue'),
        },
        {
          path: 'reviews/:id',
          name: 'OrganizationReviews',
          component: () => import('@/views/OrgReviewsPage.vue'),
          props: true,
        },
      ],
    },
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      props: { showFooter: false },
      children: [
        {
          path: 'account',
          name: 'Account',
          component: Account,
          meta: { requiresAuth: true, loadCounter: true },
          redirect: '/account/notifications',
          children: [
            {
              path: 'notifications',
              name: 'notifications',
              component: Notifications,
            },
            {
              path: 'statistics',
              name: 'statistics',
              component: Statistics,
            },
            {
              path: 'calendar',
              name: 'calendar',
              component: Calendar,
            },
            {
              path: 'my-courses',
              name: 'my-courses',
              component: MyCourses,
            },
            {
              path: 'my-courses-feedbacks',
              name: 'my-courses-feedbacks',
              component: () => import('@/views/account/my-courses-feedbacks/index.vue'),
            },
            {
              path: 'purchased-courses',
              name: 'purchased-courses',
              component: PurchasedCourses,
            },
            {
              path: 'profile',
              name: 'profile',
              component: Profile,
            },
            {
              path: 'tariff',
              name: 'tariff',
              component: Tariff,
            },
            {
              path: 'payment-history',
              name: 'payment-history',
              component: PaymentHistory,
            },
          ],
        },
        {
          path: 'account-verification/:type',
          name: 'AccountVerification',
          component: () => import('@/views/AccountVerificationPage.vue'),
          meta: { requiresAuth: true },
        },
        {
          path: 'course-editor/:id?',
          name: 'CourseEditor',
          component: () => import('@/views/CourseEditorPage.vue'),
          props: true,
          meta: { requiresAuth: true },
        },
        {
          path: '/:pathMatch(.*)*',
          name: 'NotFound',
          component: () => import('@/views/NotFoundPage.vue'),
        },
      ],
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginPage.vue'),
    },
    {
      path: '/reset-password',
      name: 'SuccessResetPasswordPage',
      component: () => import('@/views/SuccessResetPasswordPage.vue'),
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/RegisterPage.vue'),
    },
    {
      path: '/confirm-register',
      name: 'SuccessRegisterPage',
      component: () => import('@/views/SuccessRegisterPage.vue'),
    },
    {
      path: '/activate/:uid/:token',
      name: 'ActivateAccount',
      component: () => import('@/views/ActivateAccountPage.vue'),
      props: true,
    },
    {
      path: '/password/reset/confirm/:uid/:token',
      name: 'PasswordResetConfirm',
      component: () => import('@/views/PasswordResetConfirmPage.vue'),
      props: true,
    },
    {
      path: '/users/set_password_confirm/:uid/:token',
      name: 'ActivateChangePassword',
      component: () => import('@/views/ActivateChangePasswordPage.vue'),
      props: true,
    },
    {
      path: '/users/set_email_confirm/:uid/:token',
      name: 'ActivateChangeEmail',
      component: () => import('@/views/ActivateChangeEmailPage.vue'),
      props: true,
    },
  ],
  scrollBehavior() {
    return { top: 0, left: 0 }
  },
})

export default router
