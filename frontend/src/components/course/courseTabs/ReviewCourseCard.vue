<script setup lang="ts">import RatingBlock from "@/components/common/RatingBlock.vue";
import {ref} from "vue";
import {AppColors} from "@/enums/appColors.ts";
import type { IFeedback } from "@/api/feedbacks/models";
import { stubDocumentsIcon } from '@/assets/icons'

const props = defineProps<{
  review: IFeedback
}>()

const showReply = ref(false) // Управление отображением блока для ответа
const submitted = ref(false) // Флаг, чтобы показать отправленный блок
const isEditing = ref(false) // Флаг, чтобы войти в режим редактирования
const replyText = ref('') // Текст ответа

// Открыть/закрыть блок для ответа
const toggleReply = () => {
  showReply.value = !showReply.value
}

const closeReply = () => {
  showReply.value = false
  replyText.value = ''
}

// Отправка ответа
const sendReply = () => {
  if (replyText.value.trim() !== '') {
    submitted.value = true
    // showReply.value = false;
    isEditing.value = false
  }
}

// Редактирование ответа
const editReply = () => {
  isEditing.value = true
  showReply.value = true
  submitted.value = false
}
</script>

<template>
  <v-card v-if="review" elevation="0" class="d-flex flex-column pa-6 rounded-lg elevation-2 border-sm">
    <v-card-title class="d-flex flex-column flex-lg-row align-center justify-space-between pa-0 ">
      <div class="d-flex align-center ga-4">
        <v-avatar size="40" rounded="lg" icon="$vuetify" :image="props.review.feedback_author.photo || stubDocumentsIcon"></v-avatar>
        <div class="card-title">{{ props.review.feedback_author.first_name + ' ' + props.review.feedback_author.last_name }}</div>
      </div>
      <RatingBlock classes="mt-2" :rating="props.review.feedback_rating"/>
    </v-card-title>

    <v-card-text class="mt-4 pa-0 card-text  mb-2">
      {{ props.review.feedback_text }}
    </v-card-text>

    <v-card-actions class="d-flex justify-space-between pa-0 card-action-block mt-auto">
      <v-btn height="24" variant="text" class="answer-button px-0" @click="toggleReply">
        <v-icon size="18">mdi-message-text-outline</v-icon>
        Ответить
      </v-btn>
      <span class="time-ago">{{ props.review.time_ago }}</span>
    </v-card-actions>
  </v-card>

  <transition name="fade">
    <v-card
      v-if="showReply"
      class="mt-4 py-o pr-0 pl-16 position-relative d-flex ga-4"
      elevation="0"
      height="104"
    >
      <v-icon :color="AppColors.BASE_COLOR_100" size="28" class="arrow-icon"
        >mdi-subdirectory-arrow-right</v-icon
      >
      <v-textarea
        variant="outlined"
        class="textarea-block"
        v-model="replyText"
        rows="3"
        no-resize
        rounded="lg"
        v-if="!submitted"
      />
      <div v-if="!submitted" class="d-flex flex-column justify-space-between">
        <v-btn icon variant="outlined" rounded="lg" size="32" @click="sendReply">
          <v-icon>mdi-check</v-icon>
        </v-btn>
        <v-btn icon variant="outlined" rounded="lg" size="32" @click="closeReply">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </div>
      <div v-if="submitted" class="pa-3 w-100 review-content">
        <div class="d-flex align-content-start flex-fill">
          <div class="flex-fill lg">{{ replyText }}</div>
          <v-btn icon variant="text" elevation="0" @click="editReply" height="24" size="24">
            <v-icon>mdi-square-edit-outline</v-icon>
          </v-btn>
        </div>
        <div class="d-flex justify-space-between grey--text text-body-2 mt-2">
          <span>2 нед. назад</span>
          <span>отред. 3 дня назад</span>
        </div>
      </div>
    </v-card>
  </transition>
</template>

<style scoped>
.card-title {
  font-size: 24px;
  font-style: normal;
  font-weight: 700;
  line-height: 32px;
}

.card-text {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px; /* 150% */
}

.card-action-block {
  min-height: unset;
}

.answer-button {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
  text-transform: none;
}

.answer-button .v-icon {
  color: var(--Base-color-80, rgba(54, 57, 64, 0.8));
  margin-right: 8px;
}

.textarea-block {
  border-radius: 12px !important;
  background: var(--Base-color-5, rgba(54, 57, 64, 0.05));
  min-height: unset;
  height: 104px;
}

::v-deep(.v-input__details) {
  display: none;
}

::v-deep(.v-input__control) {
  min-height: unset;
  height: 104px !important;
}

.time-ago {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
  color: var(--Base-color-80, rgba(54, 57, 64, 0.8));
}

.arrow-icon {
  position: absolute;
  left: 20px;
  top: 4px;
}
.review-content {
  height: 104px;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
