<script setup lang="ts">
import type { IUniversityOrgranization } from '@/api/vuz/models'
import { useFormat } from '@/composable/useFormat'
import { usePluralize } from '@/composable/usePluralize'
import { logoBaseIcon } from '@/assets/icons'

const props = withDefaults(
  defineProps<{
    university: IUniversityOrgranization
    hideProgramsCount?: boolean
  }>(),
  {
    hideProgramsCount: false,
  },
)

const { formatNumber, firstLetterLowerDot } = useFormat()
const { pluralize } = usePluralize()
</script>

<template>
  <div class="university-card">
    <div class="university-card__left">
      <v-avatar class="university-card__avatar">
        <v-img :cover="false" :src="props.university.logo || logoBaseIcon" alt="logo">
          <template #error>
            <v-img :cover="false" :src="logoBaseIcon"></v-img>
          </template>
        </v-img>
      </v-avatar>

      <div class="university-card__description">
        <div>
          <h6 class="university-card__title">{{ props.university.short_name }}</h6>
          <span class="university-card__type">{{ props.university.organization_type }}</span>
        </div>

        <span v-if="props.university.city?.name" class="university-card__address">
          <span v-if="props.university.city.city_type">
            {{ firstLetterLowerDot(props.university.city.city_type) }}
          </span>
          {{ props.university.city.name }}
        </span>
      </div>
    </div>

    <div class="university-card__right">
      <span
        v-if="!props.hideProgramsCount && props.university.calculation_data"
        class="university-card__programs-count"
      >
        {{ formatNumber(props.university.programs_count) }}
        {{
          pluralize(props.university.calculation_data.specialties_count, [
            'программа',
            'программы',
            'программ',
          ])
        }}
      </span>
      <h6 v-if="props.university.calculation_data" class="university-card__payment">
        от {{ formatNumber(props.university.calculation_data.cost_min) }} ₽/год
      </h6>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.university-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  gap: 32px;
  cursor: pointer;

  @include md {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  &__left {
    display: flex;
    align-items: center;
    gap: 32px;
    width: 100%;

    @include md {
      gap: 16px;
    }
  }

  &__avatar {
    width: 72px;
    height: 72px;

    @include md {
      width: 64px;
      height: 64px;
    }
  }

  &__description {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  &__type,
  &__address {
    @include typography('sm');
    color: $base-60;
  }

  &__title {
    @include typography('h6');

    @include md {
      @include typography('lgb');
    }
  }

  &__right {
    display: flex;
    align-items: center;
    gap: 32px;

    @include md {
      gap: 16px;
      justify-content: space-between;
      width: 100%;
    }
  }

  &__programs-count,
  &__payment {
    min-width: 240px;
    text-align: right;
  }

  &__programs-count {
    @include typography('lg');
    min-width: 240px;

    @include md {
      min-width: auto;
    }
  }

  &__payment {
    @include typography('h6');
    min-width: 240px;

    @include md {
      @include typography('lgb');
      min-width: auto;
    }
  }
}
</style>
