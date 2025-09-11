<script setup lang="ts">
import { sberBankIcon, tinkoffIcon } from '@/assets/icons/payment'
import { courseImg } from '@/assets/course'
import { AppColors } from '@/enums/appColors.ts'
// import { formatTime } from '@/utils/helpers.ts'
import { createPayments } from '@/api/payments'
import type { IPaymentCreate } from '@/api/payments/models'
import { logoBaseIcon } from '@/assets/icons'
import { computed, onMounted } from 'vue'
import { useCourseStore } from '@/stores/Course'
import { PaymentTypeEnum } from '@/enums/paymentEnum'
import BaseButton from '../common/BaseButton.vue'
import { useDisplay } from 'vuetify'
import { useUser } from '@/stores/User'
import { useSnackbarStore } from '@/stores/Snackbar'
import { useRouter, useRoute } from 'vue-router'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'
import { StatusEnum } from '@/enums/statusEnum'
import { useMetrika } from '@/composable/useMetrika'

const courseStore = useCourseStore()
const userStore = useUser()
const snackbarStore = useSnackbarStore()
const { xs } = useDisplay()
const router = useRouter()
const route = useRoute()
const paymenySistemIconArray = [sberBankIcon, tinkoffIcon]
const { coursePurchase, coursePayment } = useMetrika()

const tags = computed(() => {
  if (!courseStore.course) return []

  const tags = courseStore.course.tag?.split(',').map((tag) => ({ name: tag })) ?? []

  return [
    ...courseStore.course.learning_types,
    ...courseStore.course.age_category,
    ...courseStore.course.course_formats,
    ...courseStore.course.learning_reasons,
    ...tags,
  ]
})

const reloadWithSuccessPay = () => {
  router
    .replace({
      path: route.path,
      query: { ...route.query, is_success_pay: 'true' },
    })
    .then(() => {
      window.location.reload()
    })
}

function showSuccesSnuck() {
  snackbarStore.showSnackbar({
    title: 'Покупка успешна!',
    message: 'Поздравляем! Вы успешно приобрели курс. Готовы начать обучение?',
    action: { label: 'Посмотреть', onClick: () => router.push('/account/purchased-courses') },
    timeout: 7000,
  })
}

async function buyCourse() {
  if (!courseStore.course) return

  if (!userStore.getIsAuthenticated) {
    snackbarStore.showSnackbar({
      title: 'Войдите в аккаунт',
      message: 'Для покупки курса вам нужно войти в свой аккаунт',
      action: { label: 'Войти', onClick: () => router.push('/login') },
      timeout: 7000,
    })
    return
  }

  const body: IPaymentCreate = {
    item_id: courseStore.course.id,
    payment_type: PaymentTypeEnum.COURSE_PURCHASE,
    amount: courseStore.course.price || '0',
  }

  try {
    coursePurchase(courseStore.course.id)
    const response = await createPayments(body)

    if (!response || typeof response !== 'object' || Object.keys(response).length === 0) {
      throw new Error('Пустой ответ от сервера')
    }

    if ('id' in response && response.status === StatusEnum.COMPLETED) {
      reloadWithSuccessPay()
    }

    if ('confirm_url' in response) {
      window.location.href = response.confirm_url
    }
  } catch {
    snackbarStore.showSnackbar({
      title: 'Ошибка на сервере',
      type: SnackbarTypeEnum.NEGATIVE,
      timeout: 7000,
    })
  }
}

const removeQueryParam = () => {
  const newQuery = { ...route.query }
  delete newQuery.is_success_pay
  router.replace({ query: newQuery })
}

const handlePaymentStatus = () => {
  const { is_success_pay } = route.query
  const isSuccessPay = is_success_pay === 'true'
  const isFailurePay = is_success_pay === 'false'

  if (isSuccessPay) {
    showSuccesSnuck()
    if (courseStore.course) {
      coursePayment(courseStore.course.id)
    }
  } else if (isFailurePay) {
    snackbarStore.showSnackbar({
      title: 'Ошибка оплаты',
      type: SnackbarTypeEnum.NEGATIVE,
      timeout: 7000,
    })
  }

  removeQueryParam()
}

const openLink = (link: string) => {
  window.open(link, '_blank', 'noopener,noreferrer')
}

onMounted(() => {
  handlePaymentStatus()
})
</script>

<template>
  <v-row v-if="courseStore.course" class="course-main ma-0" align-content="stretch">
    <v-col cols="12" md="7" class="pa-0 pb-4 pb-md-0 pr-md-8 align-self-start">
      <v-img
        cover
        :src="courseStore.course.course_image || courseImg"
        class="course-main__img"
        :class="{ disabled: courseStore.course?.is_active === false }"
        :aspect-ratio="16 / 9"
      ></v-img>
    </v-col>
    <v-col cols="12" md="5" class="pa-0">
      <v-card class="pa-0 course-main__owner">
        <div class="align-center d-flex flex-wrap ga-4">
          <div class="align-center d-flex ga-4">
            <!-- Аватар -->

            <v-avatar class="course-main__avatar">
              <v-img
                :cover="false"
                class="course-main__avatar-img"
                :src="courseStore.course.author.logo || logoBaseIcon"
                alt="Avatar"
              />
            </v-avatar>
            <!-- Текст -->
            <div>
              <div class="course-main__owner-title">{{ courseStore.course.author.title }}</div>
              <div class="course-main__owner-subtitle">
                {{ courseStore.course.author.author_type }}
              </div>
            </div>
          </div>
          <!-- скрыто -->
          <v-btn
            v-if="false"
            height="32"
            rounded="lg"
            variant="outlined"
            text="Пожаловаться"
            class="course-main__report-error ml-auto"
            @click="courseStore.setIsReportDialog(true)"
          />
        </div>
      </v-card>
      <v-row v-if="courseStore.course?.date_start" justify="center" class="mx-0 mt-4 mt-md-7">
        <v-col cols="12" class="course-main__block-time pa-4">
          Старт {{ courseStore.course?.date_start || '-' }}
        </v-col>
      </v-row>

      <v-chip-group v-if="tags.length" multiple column class="d-flex flex-wrap mt-4">
        <v-chip
          v-for="(chip, index) in tags"
          :key="index"
          class="ma-1 course-main__tag"
          variant="outlined"
          :color="AppColors.BASE_COLOR_100"
          style="border-radius: 8px"
        >
          {{ chip?.translations || chip.name }}
        </v-chip>
      </v-chip-group>

      <div class="course-main__payment-block">
        <v-img
          v-for="(icon, index) in paymenySistemIconArray"
          :key="index"
          :src="icon"
          class="course-main__payment-icon"
        ></v-img>
      </div>

      <div v-if="!courseStore.course.is_bought" class="course-main__buy">
        <BaseButton
          class="course-main__buy-btn"
          label="Купить курс"
          :text="xs ? 'text-smb' : 'text-lgb'"
          :disabled="userStore.isAuthor"
          @click="buyCourse"
        />
        <div v-if="courseStore.course.price" class="course-main__price">
          {{ parseFloat(courseStore.course.price).toLocaleString('ru-RU') }} ₽
        </div>
      </div>
      <div v-else class="course-main__details">
        <BaseButton
          label="Подробнее"
          type="outline"
          :text="xs ? 'text-smb' : 'text-lgb'"
          @click="openLink(courseStore.course.link)"
        />
      </div>
      <BaseButton
        v-if="courseStore.course.trial_version && !courseStore.course.is_bought"
        class="course-main__try"
        label="Попробовать бесплатно"
        type="outline"
        :text="xs ? 'text-smb' : 'text-lgb'"
      />
    </v-col>
  </v-row>
</template>

<style lang="scss">
.course-main {
  &__img {
    width: 100%;
    //height: 100%;
    //height: 488px;
    border-radius: 24px;
    //@include md() {
    //  height: 320px;
    //}
    //@include xs() {
    //  height: 190px;
    //}

    &.disabled {
      filter: grayscale(1);
    }
  }

  &__avatar {
    width: 56px;
    height: 56px;

    @media (max-width: 600px) {
      width: 40px;
      height: 40px;
    }
  }

  &__owner {
    box-shadow: none;
  }

  &__owner-title {
    font-size: 16px;
    font-style: normal;
    font-weight: 300;
    line-height: 24px;
  }

  &__owner-subtitle {
    font-size: 12px;
    font-style: normal;
    font-weight: 300;
    line-height: 16px;
    color: $base-60;
  }

  &__block-time {
    border-radius: 8px;
    background: $base-5;
    font-size: 16px;
    font-style: normal;
    font-weight: 700;
    line-height: 24px;
    text-align: center;

    @media (max-width: 600px) {
      font-size: 12px;
      line-height: 16px;
    }
  }

  &__tag {
    border-color: $base-5;
  }

  &__payment-icon {
    width: 56px;
    height: 56px;
    object-fit: cover;
    flex-grow: 0;

    @include xs {
      width: 32px;
      height: 32px;
    }
  }

  &__payment-block {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    padding: 8px;
    border-radius: 8px;
    border: 1px solid $base-10;
    margin-top: 28px;

    @include xs {
      margin-top: 12px;
    }
  }

  &__buy {
    display: flex;
    gap: 16px;
    margin-top: 16px;

    & > .course-main__buy-btn,
    & > .course-main__price {
      flex: 1;
    }
  }

  &__buy-btn {
    @include xs {
      padding: 8px 0;
    }
  }

  &__price {
    @include typography('h6');
    display: flex;
    justify-content: center;
    align-items: center;
    background: $base-5;
    border-radius: 8px;
    text-align: center;
    padding: 8px;

    @include xs {
      @include typography('smb');
    }
  }

  &__details {
    margin-top: 16px;

    & > button.outline {
      width: 100%;
    }

    // @include xs {
    //   & > button.outline {
    //     padding: 6px 0;
    //   }
    // }
  }

  &__try {
    margin-top: 16px;
    width: 100%;

    @include xs {
      margin-top: 8px;

      &.outline {
        padding: 6px 0;
      }
    }
  }

  &__report-error {
    text-transform: none;
    font-size: 12px;
    font-style: normal;
    font-weight: 700;
    line-height: 16px;
    border-color: $lime;
  }
}
</style>
