export const MINUTES_IN_HOUR = 60

export function formatTime(minutes: number) {
  const formattedTime = {
    min: 0,
    hour: 0,
  }

  if (minutes < MINUTES_IN_HOUR) {
    formattedTime.min = minutes
  } else {
    formattedTime.hour = Math.floor(minutes / MINUTES_IN_HOUR)
    formattedTime.min = minutes % MINUTES_IN_HOUR
  }

  return formattedTime
}

export function extractQueryFromAPILink(link: string) {
  if (!link.length && !/\/\?/.test(link)) {
    return ''
  }

  const queryString = link.split('/?')

  return queryString[1]
}

// Функция для форматирования даты в формат YYYY-MM-DD
export const formatDate = (date: Date): string => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0') // Добавляем ведущий ноль
  const day = String(date.getDate()).padStart(2, '0') // Добавляем ведущий ноль

  return `${year}-${month}-${day}`
}

export const rules = {
  required: (value: string) => !!value || 'Required.',
  email: (value: string) => {
    const pattern =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return pattern.test(value) || 'Это должен быть e-mail.'
  },
}
