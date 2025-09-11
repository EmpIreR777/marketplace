<script setup lang="ts">
import RatingBlock from "@/components/common/RatingBlock.vue";
import type {IFeedback} from "@/api/feedbacks/models";

const props = defineProps<{
  item: IFeedback
}>()

</script>

<template>
  <v-card class="pa-2 pa-sm-4 review-card">
    <v-card-title class="review-card__title">
      {{ `${props.item.feedback_author.first_name} ${props.item.feedback_author.last_name}` }}
    </v-card-title>
    <v-card-subtitle class="review-card__subtitle">
      {{ props.item.time_ago }}
    </v-card-subtitle>
    <v-card-text class="pa-0 mt-4">
      <div class="review-card__rating pa-2 pa-sm-4 mb-4">
        <p class="review-card__rating-position">{{ props.item.feedback_to_course.title }}</p>
        <RatingBlock :classes="'mt-2'" :rating="props.item.feedback_rating"/>
      </div>
      <p class="review-card__description">
        {{ props.item.feedback_text }}
      </p>
    </v-card-text>
  </v-card>
</template>



<style scoped>
.review-card {
  width: 100%;
  user-select: none;
  box-shadow: none;
  border-radius: 16px;
  border: 1px solid var(--Base-color-10, rgba(54, 57, 64, 0.10));
  @media (max-width: 600px) {
    width: 224px;
  }
}


.review-card__title {
  font-size: 16px;
  font-weight: 700;
  line-height: 24px;
  padding: 0;

  @media (max-width: 600px) {
    font-size: 14px;
    line-height: 20px;
  }
}

.review-card__subtitle {
  margin-top: 8px;
  font-size: 12px;
  font-weight: 300;
  line-height: 16px;
  padding: 0;
}

.review-card__rating {
  border-radius: 8px;
  background: var(--Base-color-5, rgba(54, 57, 64, 0.05));

  @media (max-width: 600px) {
    display: flex;
    flex-direction: column;
  }
}

.review-card__rating-position{
  font-size: 16px;
  font-weight: 300;
  line-height: 24px;
  text-overflow: ellipsis;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  line-clamp: 1; /* Для многострочного обрезания */
  -webkit-line-clamp: 1;

  @media (max-width: 1279px) {
    text-align: center;
  }
  @media (max-width: 600px) {
    font-size: 14px;
    font-weight: 300;
    line-height: 20px;
  }
}

.review-card__description {
  text-overflow: ellipsis;
  font-size: 16px;
  font-weight: 300;
  line-height: 24px;
  min-height: 72px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  line-clamp: 3; /* Для многострочного обрезания */
  -webkit-line-clamp: 3;

  @media (max-width: 600px) {
    font-size: 14px;
    line-height: 20px;
    min-height: 60px;
  }
}
</style>
