<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useDisplay } from 'vuetify'
import { useStatisticsStore } from '@/stores/Account/statistics'
import { PeriodEnum } from '@/enums/periodEnum'
import moment from 'moment/min/moment-with-locales'
import { AppColors } from '@/enums/appColors'

moment.locale('ru')

const statisticsStore = useStatisticsStore()
const { xs } = useDisplay()

const dayTitle = computed(() => (xs.value ? '1д' : 'День'))
const weekTitle = computed(() => (xs.value ? '7д' : 'Эта неделя'))
const monthTitle = computed(() => (xs.value ? '30д' : 'Месяц'))
const yearTitle = computed(() => (xs.value ? '1г' : 'Год'))

const chart = ref<InstanceType<typeof ApexCharts> | null>(null)

function setPeriod(period: PeriodEnum) {
  statisticsStore.setPeriodFilter(period)
  statisticsStore.loadStatistics()
}

function setStartDate(date: Date) {
  statisticsStore.setStartDate(date)
  if (statisticsStore.start_date && statisticsStore.end_date) {
    statisticsStore.loadStatistics()
  }
}
function setEndDate(date: Date) {
  statisticsStore.setEndDate(date)
  if (statisticsStore.start_date && statisticsStore.end_date) {
    statisticsStore.loadStatistics()
  }
}

function updateChartOptions() {
  if (chart.value === null) return

  const data = statisticsStore.getChartSeries
  if (data !== null) {
    chart.value.updateSeries(data)
  }
}

watch(() => statisticsStore.chartData, updateChartOptions)

onMounted(() => {
  statisticsStore.loadStore()
  nextTick(() => {
    updateChartOptions()
  })
})

onUnmounted(() => {
  statisticsStore.clearStore()
})
</script>

<template>
  <v-card elevation="0" :loading="statisticsStore.isLoading" class="statistics">
    <v-card-title class="pa-0" style="white-space: wrap">
      <div class="statistics__header">
        <h6 class="statistics__header-title">Статистика по продаже ваших курсов</h6>

        <div class="statistics__header-date">
          <span
            class="underline-link"
            :class="{ active: statisticsStore.periodFilter === PeriodEnum.DAY }"
            @click="setPeriod(PeriodEnum.DAY)"
          >
            {{ dayTitle }}
          </span>
          <span
            class="underline-link"
            :class="{ active: statisticsStore.periodFilter === PeriodEnum.WEEK }"
            @click="setPeriod(PeriodEnum.WEEK)"
          >
            {{ weekTitle }}
          </span>
          <span
            class="underline-link"
            :class="{ active: statisticsStore.periodFilter === PeriodEnum.MONTH }"
            @click="setPeriod(PeriodEnum.MONTH)"
          >
            {{ monthTitle }}
          </span>
          <span
            class="underline-link"
            :class="{ active: statisticsStore.periodFilter === PeriodEnum.YEAR }"
            @click="setPeriod(PeriodEnum.YEAR)"
          >
            {{ yearTitle }}
          </span>

          <div class="d-flex align-center ga-2" style="width: 340px">
            <v-date-input
              v-model="statisticsStore.start_date"
              variant="outlined"
              :base-color="AppColors.BORDER"
              prepend-icon=""
              append-inner-icon="mdi-calendar"
              hide-details
              class="custom-input"
              placeholder="dd.mm.yyyy"
              @update:model-value="setStartDate"
            />
            -
            <v-date-input
              v-model="statisticsStore.end_date"
              variant="outlined"
              :base-color="AppColors.BORDER"
              prepend-icon=""
              append-inner-icon="mdi-calendar"
              hide-details
              class="custom-input"
              placeholder="dd.mm.yyyy"
              @update:model-value="setEndDate"
            />
          </div>
        </div>
      </div>
    </v-card-title>

    <v-card-text class="pa-0 d-flex flex-column ga-6">
      <div class="statistics__charts">
        <div class="statistics__chart-card">
          <apexchart
            ref="chart"
            height="100%"
            :options="statisticsStore.getAreaChartOptions"
            :series="statisticsStore.getChartSeries"
            class="statistics__chart"
          ></apexchart>
        </div>

        <div class="statistics__courses-card">
          <div
            v-for="item of statisticsStore.getCourseStats"
            :key="item.name"
            class="statistics__courses-card-progress"
            :style="{ width: `${item.percent}%` }"
          >
            <span class="text-truncate">{{ item.name }}</span>
            <b>{{ item.total_purchases }}</b>
          </div>
          <span v-if="!statisticsStore.getCourseStats?.length" class="statistics__rating-card-title"
            >Нет данных</span
          >
        </div>
      </div>

      <div class="statistics__ratings">
        <div class="statistics__rating-card">
          <span class="statistics__rating-card-title">Лучший день</span>
          <div v-if="statisticsStore?.statistics?.best_day" class="statistics__rating-card-data">
            <span class="statistics__rating-card-date">
              {{ statisticsStore?.statistics?.best_day?.total_purchases }}
            </span>
            <span class="statistics__rating-card-value">
              {{ moment(statisticsStore.statistics?.best_day.day).format('D MMMM') }}
            </span>
          </div>
          <div v-else class="statistics__rating-card-value">нет данных</div>
        </div>
        <div class="statistics__rating-card">
          <span class="statistics__rating-card-title">Лучший месяц</span>
          <div v-if="statisticsStore?.statistics?.best_month" class="statistics__rating-card-data">
            <span class="statistics__rating-card-date">
              {{ statisticsStore?.statistics?.best_month?.total_purchases }}
            </span>
            <span class="statistics__rating-card-value">
              {{ moment(statisticsStore.statistics?.best_month.month).format('MMMM') }}
            </span>
          </div>
          <div v-else class="statistics__rating-card-value">нет данных</div>
        </div>
        <div class="statistics__rating-card">
          <span class="statistics__rating-card-title">Лучший год</span>
          <div v-if="statisticsStore?.statistics?.best_year" class="statistics__rating-card-data">
            <span class="statistics__rating-card-date">
              {{ statisticsStore?.statistics?.best_year?.total_purchases }}
            </span>
            <span class="statistics__rating-card-value">
              {{ moment(statisticsStore.statistics?.best_year.year).format('YYYY') }}
            </span>
          </div>
          <div v-else class="statistics__rating-card-value">нет данных</div>
        </div>
      </div>
    </v-card-text>
  </v-card>

  <div class="statistics"></div>
</template>

<style scoped lang="scss">
.statistics {
  display: flex;
  flex-direction: column;
  gap: 24px;

  &__header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 16px;

    @include md {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }

    &-title {
      @include typography('h6');
      // max-width: 320px;
      @include md {
        // max-width: 100%;
        margin-bottom: 8px;
      }
    }

    &-date {
      @include typography('lg');
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-left: auto;

      @include md {
        justify-content: flex-start;
        flex-direction: row-reverse;
        margin-left: 0;
      }
    }
  }

  &__charts {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;

    @include md {
      grid-template-columns: 1fr;
    }
  }

  &__ratings {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
  }

  &__courses-card,
  &__rating-card,
  &__chart-card {
    border: 1px solid $base-20;
    border-radius: 16px;
  }

  &__courses-card {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 24px;

    &-progress {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 4px;
      padding: 8px;
      min-width: 50%;
      background: $gradient;
    }
  }

  &__chart-card {
    padding: 0 16px 16px 8px;

    @include md {
      min-height: 304px;
    }
  }

  &__rating-card {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 16px;
    flex: 0 0 calc(33.33% - 16px);

    @include sm {
      flex: 0 0 calc(50% - 12px);
    }

    @include xs {
      flex: 0 0 100%;
    }

    &-data {
      display: flex;
      flex-direction: column;
    }

    &-title {
      @include typography('lgb');
      color: $base-60;
    }

    &-date {
      @include typography('h6');
    }

    &-value {
      color: $base-60;
    }
  }
}
</style>
<style lang="scss">
.custom-input {
  .v-field__outline {
    border-radius: 12px;
    outline: none;
  }
}
</style>
