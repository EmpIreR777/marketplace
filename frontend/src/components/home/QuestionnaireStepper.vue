<script setup lang="ts">
import { ref, type PropType } from 'vue'
import { useQuestionnaireStore } from '@/stores/Questionnaire'
import { AppColors } from '@/enums/appColors.ts'
import FinalSlide from './questionnaireSlider/FinalSlide.vue'
import type { IQuizQuestion } from '@/api/quiz/models'

const props = defineProps({
  questionnaireData: {
    type: Array as PropType<IQuizQuestion[]>,
    required: true,
  },
  isVisible: {
    type: Boolean,
  },
})

const questionnaireStore = useQuestionnaireStore()

const selectedOptions = ref<number[]>([])
const singleOptionSelectValue = ref<number | null>(null)
const step = ref(0)

function handleSingleSelectOption(optionId: number) {
  selectedOptions.value = [optionId]
}

function handleNext() {
  questionnaireStore.setQuestionAnswerResults({
    stepId: props.questionnaireData[step.value].id,
    answers: selectedOptions.value,
  })
  selectedOptions.value = []
  singleOptionSelectValue.value = null

  step.value++
}

function handlePrev() {
  selectedOptions.value = []
  singleOptionSelectValue.value = null
  questionnaireStore.setStepBackAnswerResult(props.questionnaireData[step.value].id)

  step.value--

  selectedOptions.value =
    questionnaireStore?.getAnswersResults?.[props.questionnaireData[step.value].id] || []

  if (
    !props.questionnaireData[step.value].has_multiple_answers &&
    questionnaireStore?.getAnswersResults?.[props?.questionnaireData[step.value].id]
  ) {
    singleOptionSelectValue.value =
      questionnaireStore?.getAnswersResults[props.questionnaireData[step.value].id][0] || null
  }
}
</script>

<template>
  <v-stepper
    v-if="!questionnaireStore.getIsLastQuestion"
    v-model="step"
    :show-actions="false"
    hide-header
    class="position-relative stepper-base"
  >
    <v-window v-model="step">
      <v-window-item v-for="(item, idx) in questionnaireData" :value="idx" :key="idx">
        <v-container fluid class="questionnaire-item">
          <div class="inner-item-wrapper">
            <div class="question-number large-screen-number">{{ item.id }}</div>
            <v-card class="questionnaire-card">
              <v-card-title class="questionnaire-title d-flex">
                <div class="question-number small-screen-number">{{ item.id }}</div>
                {{ item.text }}
              </v-card-title>
              <div class="inner-card-wrapper">
                <v-card-text class="questionnaire-text">
                  <div v-if="item.has_multiple_answers">
                    <v-checkbox
                      v-for="option in item.answers"
                      :key="option.id"
                      v-model="selectedOptions"
                      :label="option.text"
                      :value="option.id"
                      class="mt-1 custom-checkbox"
                    />
                  </div>
                  <v-radio-group v-else v-model="singleOptionSelectValue">
                    <v-radio
                      v-for="option in item.answers"
                      :key="option.id"
                      :label="option.text"
                      :value="option.id"
                      class="mt-1"
                      :color="AppColors.BASE_COLOR_100"
                      @change="handleSingleSelectOption(option.id)"
                    />
                  </v-radio-group>
                </v-card-text>
                <div class="questionnaire-actions-inner-wrapper"></div>
              </div>
            </v-card>
          </div>
        </v-container>
      </v-window-item>
      <v-window-item :value="questionnaireData.length" :key="questionnaireData.length">
        <FinalSlide />
      </v-window-item>
    </v-window>
    <v-card-actions class="questionnaire-actions-wrapper" v-if="step < questionnaireData.length">
      <v-btn
        v-if="step > 0"
        @click="handlePrev"
        :disabled="step === 0"
        :color="AppColors.BASE_COLOR_100"
        class="prev-btn"
        outlined
        >Назад</v-btn
      >
      <v-btn
        @click="handleNext"
        :disabled="step === questionnaireData.length || selectedOptions.length === 0"
        :color="AppColors.BASE_COLOR_100"
        class="next-btn ml-2"
        outlined
        >Далее</v-btn
      >
    </v-card-actions>
  </v-stepper>
</template>

<style lang="scss" scoped>
.stepper-base {
  border-radius: 32px;
  background: var(--Base-color-5, rgba(54, 57, 64, 0.05));

  @include xs() {
    border-radius: 16px;
  }
}

.questionnaire-item {
  min-height: 296px;
  padding: 50px 56px;
  overflow: hidden;
  box-sizing: border-box;

  @include md() {
    padding: 50px 56px 114px 50px;
  }

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

  @include sm() {
    padding: 8px 0;
    font-size: 24px;
    line-height: 32px;
    margin-bottom: 24px;
  }

  @include xs() {
    padding: 8px 0;
    font-size: 12px;
    line-height: 16px;
    margin-bottom: 8px;
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

  @include sm() {
    width: 38px;
    height: 38px;
    font-size: 18px;
    line-height: 22px;
  }

  @include xs() {
    width: 32px;
    height: 32px;
    font-size: 16px;
    line-height: 24px;
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
    padding: 0зч;
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
  width: 320px;
  height: 106px;
  position: absolute;
  bottom: 0;
  right: 0;
  display: flex;
  justify-content: flex-end;
  padding: 0 56px 50px 8px;

  @include sm() {
    width: 100%;
    height: 80px;
    padding: 0 8px 24px 8px;
  }

  @include xs() {
    width: 100%;
    height: 56px;
    padding: 0 8px 24px 8px;
  }
}

.questionnaire-actions-inner-wrapper {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  align-self: stretch;
  width: 320px;

  @include sm() {
    width: 100%;
    position: relative;
    min-height: unset;
    height: 56px;
  }

  @include xs() {
    width: 100%;
    position: relative;
    min-height: unset;
    height: 32px;
  }
}

.prev-btn {
  width: 64px;
  font-size: 12px;
  border-radius: 12px;
  font-style: normal;
  font-weight: 700;
  line-height: 16px;
  text-transform: none;
  height: 56px !important;

  @include sm() {
    position: absolute;
    left: 8px;
    bottom: 24px;
  }

  @include xs() {
    padding: 0 16px;
    border-radius: 8px;
    height: 32px !important;
    font-size: 12px;
    line-height: 16px;
  }
}

.next-btn {
  width: 176px;
  border-radius: 12px;
  background: var(--Accent-color-Lime-100, #df3);
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
  text-transform: none;
  height: 56px !important;

  @include sm() {
    position: absolute;
    right: 8px;
    bottom: 24px;
  }

  @include xs() {
    padding: 0 16px;
    border-radius: 8px;
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

.custom-checkbox {
  color: var(--Base-color-80, rgba(54, 57, 64, 0.8));
}
</style>
