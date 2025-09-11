<script setup lang="ts">
import { AppColors } from '@/enums/appColors.ts'
import RatingBlock from '@/components/common/RatingBlock.vue'
import { useDisplay } from 'vuetify'
import type { IAuthorForFeedback } from '@/api/autor-feedbacks/models'

defineProps<{
  organization: IAuthorForFeedback
  isCollapsed?: boolean
}>()

const { mdAndUp } = useDisplay()
</script>

<template>
  <div class="org-row" :class="isCollapsed ? 'collapsed' : ''">
    <div class="org-row__txt">
      <div class="d-flex ga-4 ga-md-8 align-start">
        <v-img
          :width="mdAndUp ? 72 : 64"
          :min-width="mdAndUp ? 72 : 64"
          :max-width="mdAndUp ? 72 : 64"
          aspect-ratio="1"
          contain
          :src="organization.logo ?? 'https://cdn.vuetifyjs.com/images/parallax/material.jpg'"
          class="rounded-circle"
          :color="AppColors.BASE_COLOR_5"
        />
        <div class="flex-fill">
          <div
            class="text-body-1 text-md-h5 font-weight-bold"
            :style="{ color: AppColors.MAIN_TEXT }"
          >
            {{ organization.title }}
          </div>
          <div class="text-caption font-weight-light mb-1" :style="{ color: AppColors.DESCR_TEXT }">
            {{ organization.full_title }}
          </div>
          <div class="text-caption font-weight-light" :style="{ color: AppColors.DESCR_TEXT }">
            {{ organization.legal_address }}
          </div>
        </div>
      </div>
    </div>

    <div class="org-row__actions">
      <RatingBlock :rating="organization.total_rating" :show-value="true" />

      <div
        class="text-caption text-sm-body-1 font-weight-light text-no-wrap"
        :style="{ color: AppColors.SECOND_TEXT }"
      >
        {{ organization.total_feedbacks }} отзывов
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.org-row {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  padding: 1rem 0;

  @include sm {
    flex-wrap: wrap;
    gap: 1rem;
  }

  &__txt {
    flex: 1 1 100%;
  }

  &__actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 1rem;

    @include sm {
      flex-basis: 100%;
      flex-wrap: wrap;
      justify-content: space-between;
    }
  }

  &.collapsed {
    @include md {
      gap: 1rem;
    }

    .org-row__actions {
      @include md {
        flex-wrap: wrap;
      }
    }
  }
}
</style>
