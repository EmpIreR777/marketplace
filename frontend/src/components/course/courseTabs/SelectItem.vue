<script setup lang="ts">
import InnerHtmlBlock from '@/components/course/courseTabs/InnerHtmlBlock.vue'
import { useCourseStore } from '@/stores/Course'
import { useSnackbarStore } from '@/stores/Snackbar'

defineProps({
  serverHtml: String,
})

const courseStore = useCourseStore()
const snackbarStore = useSnackbarStore()

const refundHandler = () => {
  if (courseStore.course?.is_returned) {
    courseStore.setIsRefundDialog(true)
  } else {
    snackbarStore.showSnackbar({
      title: 'Автоматический возврат не возможен',
      message: 'Обратитетсь в тех.поддержку',
      timeout: 7000,
    })
    if (window.jivo_api) {
      window.jivo_api.open()
    }
  }
}
</script>

<template>
  <div class="content-wrapper pb-12 position-relative pa-0">
    <InnerHtmlBlock v-if="serverHtml" :content="serverHtml" />
    <slot></slot>
    <div class="d-flex ga-4 position-absolute left-0 bottom-0">
      <!-- скрыто -->
      <v-btn
        v-if="false"
        height="32"
        rounded="lg"
        variant="outlined"
        class="report-error"
        text="Сообщить об ошибке"
        @click="courseStore.setIsReportDialog(true)"
      />
      <v-btn
        v-if="courseStore.course?.is_bought"
        height="32"
        rounded="lg"
        variant="outlined"
        class="report-error"
        text="Вернуть"
        @click="refundHandler"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.content-wrapper {
  display: grid;
  grid-auto-columns: 100%;
  gap: 2rem;

  @include xs {
    gap: 1rem;
  }
}

.report-error {
  text-transform: none;
  font-size: 12px;
  font-style: normal;
  font-weight: 700;
  line-height: 16px;
  border: 1px solid var(--Accent-color-Lime-100);
}
</style>
