<script setup lang="ts">
import CourseHeader from '@/components/course/CourseHeader.vue'
import CourseMain from '@/components/course/CourseMain.vue'
import { useCourseStore } from '@/stores/Course'
import { onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import CourseTabs from '@/components/course/courseTabs/CourseTabs.vue'
import MobileCourseSelectBlock from '@/components/course/courseTabs/MobileCourseSelectBlock.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'
import type { IOption } from '@/api/models'
import { useFieldRules } from '@/composable/useFieldRules'
import { useSnackbarStore } from '@/stores/Snackbar'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'
import NotFoundCourse from '@/components/course/NotFoundCourse.vue'
import { AppColors } from '@/enums/appColors.ts'
import { createRefund } from '@/api/payments'
import type { IPaymentRefund } from '@/api/payments/models'

const route = useRoute()
const courseStore = useCourseStore()
const snackbarStore = useSnackbarStore()
const fieldRules = useFieldRules()

const errorTypes: IOption[] = [
  { id: 1, name: 'Некорректное описание' },
  { id: 2, name: 'Иллюзия перспективы' },
  { id: 3, name: 'Тщетность бытия' },
  { id: 4, name: 'Другая ошибка...' },
]

const isError = ref(false)
const reportForm = ref<HTMLFormElement | null>(null)
const isReportFormValid = ref(false)
const reportFormModel = reactive({
  reportType: null,
  reportMessage: null,
})

const refundForm = ref<HTMLFormElement | null>(null)
const isRefundFormValid = ref(false)
const refundReason = ref<string | null>(null)

const resetReportForm = () => {
  reportForm.value?.reset()
}

const cancelReport = () => {
  resetReportForm()
  courseStore.setIsReportDialog(false)
}

const resetRefundForm = () => {
  refundForm.value?.reset()
}

const cancelRefund = () => {
  resetRefundForm()
  courseStore.setIsRefundDialog(false)
}

const showSnackbar = (title: string, message: string, type: SnackbarTypeEnum) => {
  snackbarStore.showSnackbar({
    title,
    message,
    type,
    action: { label: 'Закрыть', onClick: () => (snackbarStore.show = false) },
    timeout: 7000,
  })
}

const submitReport = async () => {
  const { valid } = await reportForm.value?.validate()

  if (valid) {
    cancelReport()
    showSnackbar('Ok', 'Сообщение оптправлено', SnackbarTypeEnum.DEFAULT)
    return
    try {
      await apiPostReport()
      showSnackbar('Ok', 'Сообщение оптправлено', SnackbarTypeEnum.DEFAULT)
      cancelReport()
    } catch (error: unknown) {
      const title = error instanceof Error ? error.message : 'Ошибка'
      showSnackbar(title, 'Сообщение не оптправлено', SnackbarTypeEnum.NEGATIVE)
    }
  }
}

const submitRefund = async () => {
  const { valid } = await refundForm.value?.validate()

  if (valid) {
    try {
      const payload: IPaymentRefund = {
        course_id: courseStore.course?.id ?? '',
        refund_reason: refundReason.value ?? '',
      }
      await createRefund(payload)
      showSnackbar('Ok', 'Заявка на возврат отправлена', SnackbarTypeEnum.DEFAULT)
      cancelReport()
      if (courseStore.course) {
        courseStore.course.is_bought = false
      }
    } catch (error: unknown) {
      const title = error instanceof Error ? error.message : 'Ошибка'
      showSnackbar(title, 'Заявка на возврат не оптправлена', SnackbarTypeEnum.NEGATIVE)
    }
  }
}

const loadCourse = async (courseId: string) => {
  if (!courseId) return
  try {
    await courseStore.loadCourseById(courseId)
    isError.value = false // сбрасываем ошибку при успешной загрузке
  } catch (e) {
    isError.value = true
  }
}

onMounted(() => {
  loadCourse(route.params.id as string)
})

watch(
  () => route.params.id,
  (newId) => {
    loadCourse(newId as string)
  },
) // immediate: true вызовет watcher сразу при монтировании

const rating = 5
</script>

<template>
  <div v-if="!isError" class="course">
    <CourseHeader v-if="courseStore.course" :title="courseStore.course.name" :rating="rating" />
    <CourseMain v-if="courseStore.course" />
    <CourseTabs v-if="courseStore.course" :course-data="courseStore.course" />
    <MobileCourseSelectBlock />
    <BaseDialog
      v-model="courseStore.isReportDialog"
      title="Сообщить об ошибке"
      cancelText="Отменить"
      confirmText="Сообщить"
      :isconfirmDisabled="!isReportFormValid"
      @cancel="cancelReport"
      @confirm="submitReport"
    >
      <template #default>
        <v-form ref="reportForm" v-model="isReportFormValid">
          <div class="text-caption font-weight-light mb-4">Выберите подходящий пункт</div>
          <v-select
            v-model="reportFormModel.reportType"
            :items="errorTypes"
            :rules="[fieldRules.required]"
            label="Тип ошибки"
            item-title="name"
            item-value="id"
            variant="outlined"
            rounded="lg"
            :base-color="AppColors.BORDER"
            class=""
          />
          <v-textarea
            v-model="reportFormModel.reportMessage"
            variant="outlined"
            label="Опишите причину"
            rows="3"
            rounded="lg"
            :base-color="AppColors.BORDER"
          />
        </v-form>
      </template>
    </BaseDialog>

    <BaseDialog
      v-model="courseStore.isRefundDialog"
      :title="`Возврат курса ${courseStore.course?.name}`"
      cancelText="Отменить"
      confirmText="Вернуть"
      :isconfirmDisabled="!isRefundFormValid"
      @cancel="cancelRefund"
      @confirm="submitRefund"
    >
      <template #default>
        <v-form ref="refundForm" v-model="isRefundFormValid">
          <v-textarea
            v-model="refundReason"
            :rules="[fieldRules.required]"
            variant="outlined"
            label="Опишите причину"
            rows="3"
            rounded="lg"
            :base-color="AppColors.BORDER"
          />
        </v-form>
      </template>
    </BaseDialog>
  </div>
  <NotFoundCourse v-else />
</template>

<style scoped lang="scss">
.course {
  display: grid;
  grid-template-columns: 100%;
  gap: 2rem;

  @include xs {
    gap: 1rem;
  }
}

::v-deep(.v-field) {
  border-radius: 12px;
}
</style>
