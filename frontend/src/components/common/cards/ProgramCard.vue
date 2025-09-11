<script setup lang="ts">
import BaseButton from '@/components/common/BaseButton.vue'
import BaseBadge from '@/components/common/BaseBadge.vue'
import BaseIcon from '@/components/common/BaseIcon.vue'
import { useFormat } from '@/composable/useFormat'
import type { IUniversityProgram } from '@/api/vuz/models'

const { formatNumber } = useFormat()

const props = defineProps<{
  program: IUniversityProgram
}>()
</script>

<template>
  <div class="program-card">
    <div class="program-card__left">
      <div class="program-card__title">
        <span class="program-card__title-faculty">{{ props.program.faculty.name }}</span>
        <h6 class="program-card__title-specialty">{{ props.program.specialty.name }}</h6>
      </div>
      <div class="program-card__conditions">
        <div class="program-card__offer-list">
          <span>{{ props.program.budget_places }} бюджетных мест</span>
          <span v-if="props.program.cost">от {{ formatNumber(props.program.cost) }} ₽ / год</span>
        </div>
        <div v-if="props.program.calculation_data?.exams_name" class="program-card__knowledge-list">
          <span>Необходимые знания</span>
          <span
            v-for="knowledge of props.program.calculation_data.exams_name.split(', ')"
            :key="knowledge"
          >
            <BaseIcon name="brand-apple" size="20px" />
            {{ knowledge }}
          </span>
        </div>
      </div>
    </div>
    <div class="program-card__right">
      <BaseBadge
        v-if="props.program.specialty.level_code"
        :content="props.program.specialty.level_code"
        variant="grey"
      />
      <BaseButton label="Хочу поступить" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.program-card {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 16px;
  border: 1px solid $base-10;
  border-radius: 16px;

  @include xs {
    flex-direction: column;
  }

  &__left,
  &__right {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  &__right {
    align-items: center;
    justify-content: space-between;
    flex: 1;
    max-width: 264px;
    min-width: 264px;

    @include xs {
      align-items: flex-start;
      max-width: none;
      min-width: none;
      width: 100%;
      gap: 8px;
    }

    & > .base-button {
      padding: 16px;
      width: 100%;
    }
  }

  &__title {
    display: flex;
    flex-direction: column;

    &-faculty {
      color: $base-80;
    }

    &-specialty {
      @include typography('h6');
    }
  }

  &__conditions {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  &__offer-list {
    display: flex;
    gap: 16px;

    @include xs {
      flex-direction: column;
    }
  }

  &__knowledge-list {
    display: flex;
    column-gap: 8px;
    flex-wrap: wrap;

    & > span {
      display: flex;
      gap: 4px;
    }
  }
}
</style>
