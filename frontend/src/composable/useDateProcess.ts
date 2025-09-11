import type { DateRangeModel } from '@/types/index'

interface DateProcessComposition {
  getDateArray: (dateRange: DateRangeModel) => Date[]
}

export function useDateProcess(): DateProcessComposition {
  const getDateArray = (dateRange: DateRangeModel): Date[] => {
    const { start_date, end_date } = dateRange

    if (!start_date || !end_date) {
      return []
    }

    const startDate = new Date(start_date)
    const endDate = new Date(end_date)

    if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
      return []
    }

    const dateArray: Date[] = []
    const currentDate = new Date(startDate)

    while (currentDate <= endDate) {
      dateArray.push(new Date(currentDate))
      currentDate.setDate(currentDate.getDate() + 1)
    }

    return dateArray
  }

  return {
    getDateArray,
  }
}
