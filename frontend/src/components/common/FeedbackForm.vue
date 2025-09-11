<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useFieldRules } from '@/composable/useFieldRules'
import { useSnackbarStore } from '@/stores/Snackbar'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'
import { AppColors } from '@/enums/appColors.ts'
import BaseButton from '@/components/common/BaseButton.vue'
import { postFeedback } from '@/api/feedbacks'
import type { IPpostFeedback } from '@/api/feedbacks/models'
import { useMetrika } from '@/composable/useMetrika'

const props = defineProps<{
  courseId: string
}>()

const emits = defineEmits<{
  (e: 'cancel'): void
}>()

const snackbarStore = useSnackbarStore()
const fieldRules = useFieldRules()
const { courseReview } = useMetrika()

const form = ref<HTMLFormElement | null>(null)
const isFormValid = ref(false)
const formModel = reactive({
  feedback_rating: 0,
  feedback_text: '',
})

const cancelForm = () => {
  form.value?.reset()
  emits('cancel')
}

const showSnackbar = (title: string, message: string, type: SnackbarTypeEnum) => {
  snackbarStore.showSnackbar({
    title,
    message,
    type,
    action: { label: 'Закрыть', onClick: () => (snackbarStore.show = false) },
  })
}

const submitForm = async () => {
  const { valid } = await form.value?.validate()
  const payload: IPpostFeedback = { ...formModel, feedback_to_course: props.courseId }

  if (valid) {
    try {
      await postFeedback(payload)
      showSnackbar('Ok', 'Отзыв оптправлен', SnackbarTypeEnum.DEFAULT)
      cancelForm()
      courseReview(props.courseId)
    } catch (error: unknown) {
      const title = error instanceof Error ? error.message : 'Ошибка'
      showSnackbar(title, 'Отзыв не оптправлен', SnackbarTypeEnum.NEGATIVE)
    }
  }
}
</script>

<template>
  <v-card elevation="0" class="d-flex flex-column ga-4">
    <v-card-text class="pa-0">
      <v-form ref="form" v-model="isFormValid" class="d-flex flex-column ga-4">
        <div
          class="d-flex flex-wrap justify-space-between ga-4 pa-4"
          style="border-radius: 12px"
          :style="{ border: `1px solid ${AppColors.BORDER}`, color: AppColors.SECOND_TEXT }"
        >
          <div class="text-body-1 font-weight-medium">Рейтинг (чем больше тем лучше)</div>

          <v-rating
            v-model="formModel.feedback_rating"
            hover
            :length="5"
            :size="24"
            :color="AppColors.MAIN_TEXT"
            :active-color="AppColors.ACCENT_COLOR_LIME_100"
          />
          <v-text-field
            v-model="formModel.feedback_rating"
            :rules="[fieldRules.isGreatZero]"
            readonly
            class="d-none"
          />
        </div>

        <v-textarea
          v-model="formModel.feedback_text"
          :rules="[fieldRules.required]"
          variant="outlined"
          label="Отзыв"
          rows="3"
          rounded="lg"
          :base-color="AppColors.BORDER"
          class=""
        />
      </v-form>
    </v-card-text>

    <v-card-actions class="pa-0 ga-4 ga-md-8">
      <BaseButton class="flex-fill ma-0" label="Отмена" type="outline" @click="cancelForm" />
      <BaseButton
        class="flex-fill ma-0"
        label="Оставить отзыв"
        :disabled="!isFormValid"
        @click="submitForm"
      />
    </v-card-actions>
  </v-card>
</template>

<style></style>
