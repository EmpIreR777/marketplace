import { defineStore } from 'pinia'
import { type IStatisticsStoreModel } from '@/stores/Account/statistics/models'
import { getPaymentsStatistics } from '@/api/payments'
import type { IPaymentStatisitcs, IPayStatPurchaseHistory } from '@/api/payments/models'
import { PeriodEnum } from '@/enums/periodEnum'
import { PARAMS_DATE_FORMAT } from '@/enums/dateEnum'
import { useRouter } from 'vue-router'
import type { Recordable } from '@/types'
import moment from 'moment'

export const useStatisticsStore = defineStore('statisticsStore', {
  state: (): IStatisticsStoreModel => {
    return {
      statistics: null,
      chartData: [],
      areaSeries: [],
      areaCategories: [],
      start_date: null,
      end_date: null,
      periodFilter: null,
      isLoading: false,
      router: useRouter(),
    }
  },

  getters: {
    getDateAgo(state) {
      return state.periodFilter
        ? moment(new Date()).subtract(1, state.periodFilter).toDate()
        : new Date()
    },

    getDateRangeParams(state) {
      if (!state.start_date || !state.end_date) return null

      return {
        start_date: moment(state.start_date).format(PARAMS_DATE_FORMAT),
        end_date: moment(state.end_date).format(PARAMS_DATE_FORMAT),
      }
    },

    getAreaChartOptions() {
      return {
        chart: {
          type: 'area',
          toolbar: {
            show: false,
          },
          locales: [
            {
              name: 'ru',
              options: {
                months: [
                  'Январь',
                  'Февраль',
                  'Март',
                  'Апрель',
                  'Май',
                  'Июнь',
                  'Июль',
                  'Август',
                  'Сентябрь',
                  'Октябрь',
                  'Ноябрь',
                  'Декабрь',
                ],
                shortMonths: [
                  'Янв',
                  'Фев',
                  'Мар',
                  'Апр',
                  'Май',
                  'Июн',
                  'Июл',
                  'Авг',
                  'Сен',
                  'Окт',
                  'Ноя',
                  'Дек',
                ],
                days: [
                  'Воскресенье',
                  'Понедельник',
                  'Вторник',
                  'Среда',
                  'Четверг',
                  'Пятница',
                  'Суббота',
                ],
                shortDays: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
                toolbar: {
                  exportToSVG: 'Сохранить SVG',
                  exportToPNG: 'Сохранить PNG',
                  exportToCSV: 'Сохранить CSV',
                  menu: 'Меню',
                  selection: 'Выбор',
                  selectionZoom: 'Выбор и увеличение',
                  zoomIn: 'Приблизить',
                  zoomOut: 'Отдалить',
                  pan: 'Перемещение',
                  reset: 'Сбросить масштаб',
                },
              },
            },
          ],
          defaultLocale: 'ru',
        },
        dataLabels: {
          enabled: false,
        },
        colors: ['#ddff33'],
        stroke: {
          curve: 'straight',
          show: false,
        },
        grid: {
          xaxis: {
            lines: {
              show: true,
            },
          },
          yaxis: {
            lines: {
              show: true,
            },
          },
        },
        xaxis: {
          type: 'datetime',
        },
        tooltip: {
          enabled: false,
        },
      }
    },

    getChartSeries(state) {
      return [
        {
          data: state.chartData,
        },
      ]
    },

    getCourseStats(state) {
      const maxValue = Math.max(
        ...(state.statistics?.course_stats.map((item) => item.total_purchases) ?? []),
      )
      const percent = (value: number) => (value * 100) / maxValue

      return state.statistics?.course_stats
        .sort((a, b) => b.total_purchases - a.total_purchases)
        .map((el) => {
          return {
            ...el,
            percent: percent(el.total_purchases),
          }
        })
    },
  },

  actions: {
    setPeriodFilter(value: PeriodEnum) {
      this.periodFilter = value
      this.start_date = this.getDateAgo
      this.end_date = new Date()

      this.updateRoute()
    },

    setStartDate(date: Date) {
      this.periodFilter = null
      this.start_date = date
      this.updateRoute()
    },
    setEndDate(date: Date) {
      this.periodFilter = null
      this.end_date = date
      this.updateRoute()
    },

    setStatistics(data: IPaymentStatisitcs) {
      this.statistics = data
    },

    setChartData(value: IPayStatPurchaseHistory[]) {
      this.chartData = value.map((el) => {
        return {
          x: el.day,
          y: el.total_purchases,
        }
      })
    },

    updateRoute() {
      const query: Recordable = {}
      if (!this.getDateRangeParams) return
      const { start_date, end_date } = this.getDateRangeParams

      query.start_date = moment(start_date).format(PARAMS_DATE_FORMAT)
      query.end_date = moment(end_date).format(PARAMS_DATE_FORMAT)
      this.router.replace({ query })
    },

    loadRouteParams() {
      const query = this.router.currentRoute.query
      const { start_date, end_date } = query || {}

      if (start_date && end_date) {
        this.start_date = moment(String(start_date)).toDate()
        this.end_date = moment(String(end_date)).toDate()
      }
    },

    async loadStatistics() {
      try {
        this.isLoading = true
        const dateRange = this.getDateRangeParams
        const response = await getPaymentsStatistics(dateRange ? { ...dateRange } : undefined)
        this.setStatistics(response)
        this.setChartData(response.purchase_history)
      } finally {
        this.isLoading = false
      }
    },

    async loadStore() {
      this.loadRouteParams()
      this.loadStatistics()
    },

    clearStore() {
      this.statistics = null
      this.chartData = []
      this.areaSeries = []
      this.areaCategories = []
      this.periodFilter = null
      this.start_date = null
      this.end_date = null
      this.isLoading = false
    },
  },
})
