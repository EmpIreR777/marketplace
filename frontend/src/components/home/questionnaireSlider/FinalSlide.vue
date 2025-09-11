<script setup lang="ts">
import {useRouter} from "vue-router";
import { postQuizAnswer } from '@/api/quiz';
import {AppColors} from "@/enums/appColors.ts"
import { useQuestionnaireStore } from '@/stores/Questionnaire';
import { extractQueryFromAPILink } from '@/utils/helpers';

const router = useRouter();
const questionnaireStore = useQuestionnaireStore()

const handlerGetResult = async () => {
  const body = {
    quiz: {
      ...questionnaireStore.getAnswersResults
    }
  }
  const getResultFilters = await postQuizAnswer(body)
  await router.push(`/courses/?${extractQueryFromAPILink(getResultFilters.url)}`);
}

</script>

<template>
  <v-container fluid class="questionnaire-item">
    <v-row class="h-100 ma-0" justify="end" align-content="space-between">
      <h3 class="title">На основе Ваших ответов мы подобрали лучшие курсы для Вас!</h3>
      <div class="mt-4">
        <v-btn :color="AppColors.ACCENT_COLOR_LIME_100" class="next-btn" outlined @click="handlerGetResult">
          Посмотреть
        </v-btn>
      </div>
    </v-row>
  </v-container>
</template>

<style lang="scss" scoped>

.questionnaire-item {
  display: flex;
  flex-direction: column;
  min-height: 296px;
  padding: 50px 56px;
  border-radius: 32px;
  background: var(--Base-color-5, rgba(54, 57, 64, 0.05));
  overflow: hidden;

  @include sm() {
    padding: 24px 28px;
  }

  @include xs() {
    min-height: 244px !important;
    padding: 24px 8px;
    border-radius: 16px;
  }
}

.title{
  font-size: 64px;
  font-weight: 700;
  line-height: 72px;

  @include md() {
    font-size: 48px;
    line-height: 52px;
  }

  @include sm() {
    font-size: 36px;
    line-height: 42px;
  }

  @include xs() {
    font-size: 24px;
    line-height: 32px;
  }
}

.next-btn{
  width: 176px;
  height: 56px !important;
  // padding: 16px 32px;
  border-radius: 12px;
  background: var(--Accent-color-Lime-100, #DF3);
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
  text-transform: none;

  @include xs() {
    padding: 0 16px;
    border-radius: 8px;
    width: auto;
    height: 32px !important;
    font-size: 12px;
    line-height: 16px;
  }
}
</style>
