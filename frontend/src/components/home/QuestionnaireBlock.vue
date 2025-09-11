<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuestionnaireStore } from '@/stores/Questionnaire'
import { quotes } from '@/assets/home'
import { arrowRightIcon } from '@/assets/icons'
// import QuestionnaireSlider from "./questionnaireSlider/QuestionnaireSlider.vue";
import QuestionnaireStepper from './QuestionnaireStepper.vue'
import QuestionnaireMainScreen from './QuestionnaireMainScreen.vue'
// import { useUser } from '@/stores/User';
// import { getQuizQuestion } from '@/api/quiz';
// import type { IQuizQuestion } from '@/api/quiz/models';

const questionnaireStore = useQuestionnaireStore()
// const user = useUser()

const isHidden = ref(false)
const isVisible = ref<boolean>(false)

const handleStartPoll = () => {
  // if (!user.user.id) {
  //   return
  // }
  isHidden.value = true
  setTimeout(() => {
    isVisible.value = true
  }, 300)
}
onMounted(async () => {
  await questionnaireStore.loadQuestionnaireQuestions()

  questionnaireStore.resetQuestionnaireQuizAnswersResults()
})
</script>

<template>
  <div class="mb-10 mb-sm-0">
    <v-row class="ma-0">
      <v-col class="your-way-title">
        <h5 class="heading_h5 your-way-title__txt">Начните свой путь</h5>
        <h5 class="heading_h5 your-way-title__txt">
          к новым вершинам знаний <span class="headline">с EdX</span>
        </h5>
        <v-img cover :src="quotes" class="title-img"></v-img>
      </v-col>
    </v-row>
    <v-row class="mt-6 mb-0 mx-n2 mx-sm-0">
      <v-col class="pa-0 position-relative questionnaire-block">
        <QuestionnaireMainScreen :isHidden="isHidden" />
        <v-btn v-if="!isHidden" class="start-slider-btn" @click="handleStartPoll">
          <v-img
            :width="24"
            :height="24"
            aspect-ratio="1/1"
            cover
            :src="arrowRightIcon"
            rounded="circle"
          ></v-img>
        </v-btn>

        <QuestionnaireStepper
          :isVisible="isVisible"
          :questionnaireData="questionnaireStore.getQuestionnaireQuestions || []"
          v-if="isVisible"
        />
      </v-col>
    </v-row>
  </div>
</template>

<style lang="scss" scoped>
.your-way-title {
  position: relative;
  padding: 112px 0;

  @include sm() {
    padding: 32px 28px;
  }

  &__txt {
    position: relative;
    z-index: 1;
  }
}

.your-way-title h5 {
  font-size: 32px;
  line-height: 48px;
  font-weight: 300;
  text-align: center;

  @include sm() {
    font-size: 16px;
    line-height: 24px; /* 150% */
  }
}

.your-way-title h5 span {
  font-weight: 900;

  @include sm() {
    font-weight: 700;
  }
}

.title-img {
  width: 241px;
  height: 172px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  @include sm() {
    width: 81px;
    height: 58px;
  }
}

.questionnaire-block {
  width: 100%;
  min-height: 396px;

  @include xs() {
    min-height: 160px;
  }
}

.start-slider-btn {
  padding: 0;
  position: absolute;
  right: 156px;
  bottom: -64px;
  display: flex;
  width: 128px;
  height: 128px;
  justify-content: center;
  align-items: center;
  border-radius: 999px;
  background: linear-gradient(
    to bottom,
    /* Градиент сверху вниз */ rgba(255, 255, 255, 0.1) 0%,
    /* Слабый белый вверху */ rgba(255, 255, 255, 0.8) 100% /* Почти белый внизу */
  );
  box-shadow: 0 5px 10px rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(32px);
  z-index: 1000;

  @include sm() {
    width: 80px;
    height: 80px;
    bottom: -40px;
    right: 20px;
  }

  @include xs() {
    width: 40px;
    height: 40px;
    bottom: -20px;
    right: 20px;
    background: var(--Accent-color-Lime-100, #df3);
  }
}

::v-deep(.v-btn--size-default) {
  min-width: 40px;
}
</style>
