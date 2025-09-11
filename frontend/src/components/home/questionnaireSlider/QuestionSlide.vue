<script setup lang="ts">
import {ref} from "vue";
import {AppColors} from "@/enums/appColors.ts"
import type { IQuizQuestion } from '@/api/quiz/models'
import { useQuestionnaireStore } from '@/stores/Questionnaire';
import {
  // getQuizQuestion,
  // postQuizAnswer
} from '@/api/quiz';

const props = defineProps({
  data: {
    type: Object as () => IQuizQuestion,
    required: true,
  },
});

const emit = defineEmits(['prev', 'next']);

const questionnaireStore = useQuestionnaireStore()

const singleOptionSelectValue = ref(null)

function handleSingleSelectOption(optionId: number) {
  selectedOptions.value = [optionId]
}

const selectedOptions = ref<number[]>([]);

function clearSelectedAnswers() {
  selectedOptions.value = []
}

async function handleBackButton() {
  // await questionnaireStore.stepBackQuestionnaireQuizQuestion(props.data)
  // const response = await getQuizQuestion()
  // if (response.hasOwnProperty('id')) {
  //   questionnaireStore.setQuestionnaireQuizQuestion(response as IQuizQuestion)
  //   questionnaireStore.setQuestionAnswerResults({id: props.data.id, answers: selectedOptions.value})
  // }
  if (singleOptionSelectValue.value) {
    singleOptionSelectValue.value = null
  }

  clearSelectedAnswers()

  emit('prev')
}

async function handleNextButton() {
  if (selectedOptions.value.length === 0) {
    return
  }

  questionnaireStore.setQuestionAnswerResults({id: props.data.id, answers: selectedOptions.value})
  // postQuizAnswer({ answer_ids: selectedOptions.value})
    // .then(() => { return getQuizQuestion() })
    // .then((response) => {
    //   if (response.hasOwnProperty('id')) {
    //       questionnaireStore.setQuestionnaireQuizQuestion(response as IQuizQuestion)
    //     }

    //   if (response.hasOwnProperty('results')) {
    //       questionnaireStore.setIsLastQuestion(true)
    //     }
    //   return response
    // })

    // postQuizAnswer()
    // .then(() => {
      // if (data.hasOwnProperty('id')) {
        emit('next')
      // }
  // })
}

</script>

<template>
  <v-container fluid class="questionnaire-item">
    <div class="inner-item-wrapper">
      <div class="question-number large-screen-number">{{ props.data.id }}</div>
      <v-card class="questionnaire-card">
        <v-card-title class="questionnaire-title d-flex">
          <div class="question-number small-screen-number">{{ props.data.id }}</div>
          {{props.data.text}}
        </v-card-title>
        <div class="inner-card-wrapper">
          <v-card-text class="questionnaire-text">
            <div v-if="data.has_multiple_answers">
              <v-checkbox
                v-for="(option) in props.data.answers"
                :key="option.id"
                v-model="selectedOptions"
                :label="option.text"
                :value="option.id"

                class="mt-1 custom-checkbox"
              />
            </div>
            <v-radio-group v-else v-model="singleOptionSelectValue">
              <v-radio
                v-for="(option) in props.data.answers"
                :key="option.id"
                :label="option.text"
                :value="option.id"
                class="mt-1"
                :color="AppColors.BASE_COLOR_100"
                @change="handleSingleSelectOption(option.id)"
              />
            </v-radio-group>
          </v-card-text>
          <div class="questionnaire-actions-wrapper">
            <v-card-actions>
              <v-btn v-if="props.data.id>1" :color="AppColors.BASE_COLOR_100" class="prev-btn" outlined @click="handleBackButton">
                Назад
              </v-btn>
              <v-btn :disabled="selectedOptions.length === 0" :color="AppColors.BASE_COLOR_100" class="next-btn ml-2" outlined @click="handleNextButton">
                Далее
              </v-btn>
            </v-card-actions>
          </div>
        </div>
      </v-card>
    </div>
  </v-container>
</template>

<style lang="scss" scoped>

.questionnaire-item {
  min-height: 296px;
  padding: 50px 56px;
  border-radius: 32px;
  background: var(--Base-color-5, rgba(54, 57, 64, 0.05));
  backdrop-filter: blur(12px);
  overflow: hidden;
  box-sizing: border-box;

  @include sm() {
    height: auto;
    padding: 24px 8px;
    border-radius: 16px;
  }
}

.inner-item-wrapper {
  display: flex;
  flex-direction: row;
}

.inner-card-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;

  @include md() {
    flex-direction: column;
    gap: 16px;
  }
}

.questionnaire-card {
  height: 100%;
  width: 100%;
  background: transparent;
  box-shadow: none;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  @include sm() {
    width: 100%;
    justify-content: flex-start;
  }
}

.questionnaire-title {
  font-size: 32px;
  font-weight: 700;
  line-height: 48px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  white-space: normal;
  margin-bottom: 32px;
  padding: 0 0 0 8px;

  @include xs() {
    padding: 8px 0;
    font-size: 12px;
    line-height: 16px;
  }

  @include sm() {
    padding: 8px 0;
    font-size: 24px;
    line-height: 32px;
  }
}

.question-number {
  flex-shrink: 0;
  background-color: var(--Accent-color-Lime-100);
  display: flex;
  width: 48px;
  height: 48px;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  font-weight: 700;
  line-height: 32px;
  border-radius: 999px;
  backdrop-filter: blur(32px);
  margin-right: 8px;

  @include xs() {
    width: 32px;
    height: 32px;
    font-size: 16px;
    line-height: 24px;
  }

  @include sm() {
    width: 38px;
    height: 38px;
    font-size: 18px;
    line-height: 22px;
  }
}

.large-screen-number {
  @media (max-width: 960px) {
    display: none;
  }
}

.small-screen-number {
  @media (min-width: 961px) {
    display: none;
  }
}

.questionnaire-text {
  flex: 0 0 auto;
  padding: 0;

  @include md() {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
  }

  @include xs() {
    padding: 8px 0 16px;
    min-height: unset;
    height: auto;
  }
}

::v-deep(.v-label) {
  @include xs() {
    font-size: 12px !important;
    font-weight: 300;
    line-height: 16px;
    margin-left: 4px;
  }
}

.questionnaire-actions-wrapper {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  align-self: stretch;

  @include sm() {
    position: relative;
    min-height: unset;
    height: 32px;
  }
}

.prev-btn {
  font-size: 12px;
  border-radius: 12px;
  font-style: normal;
  font-weight: 700;
  line-height: 16px;
  text-transform: none;
  height: 56px !important;

  @include sm() {
    position: absolute;
    bottom: 0;
    left: 0;
    padding: 0 16px;
    height: 32px !important;
    font-size: 12px;
    line-height: 16px;
  }
}

.next-btn {
  width: 176px;
  border-radius: 12px;
  background: var(--Accent-color-Lime-100, #DF3);
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
  text-transform: none;
  height: 56px !important;

  @include sm() {
    position: absolute;
    bottom: 0;
    right: 0;
    padding: 0 16px;
    width: auto;
    height: 32px !important;
    font-size: 12px;
    line-height: 16px;
  }
}

::v-deep(.v-input__details) {
  display: none;
}

::v-deep(.v-checkbox .v-selection-control) {
  min-height: auto;
}

.custom-checkbox{
  color: var(--Base-color-80, rgba(54, 57, 64, 0.80));
}
</style>
