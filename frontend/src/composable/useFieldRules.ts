interface FieldRulesComposition {
  required: (v: string | number | unknown[]) => boolean | string
  isUrl: (v: string, checkProtocol?: boolean) => boolean | string
  isGreatZero: (v: number) => boolean | string
  isEmail: (v: string) => boolean | string
  isPhoneNumber: (v: string) => boolean | string
  isOnlyLetters: (v: string) => boolean | string
}
export function useFieldRules(): FieldRulesComposition {
  const required = (v: string | number | unknown[]) => {
    if (Array.isArray(v)) return v.length > 0 || 'Поле обязательно для заполнения'
    return !!v || 'Поле обязательно для заполнения'
  }

  const isUrl = (v: string, checkProtocol?: boolean) => {
    if (!v || !v.length) {
      return true
    }

    // если не нужно проверять наличие протокола
    if (!checkProtocol)
      return /^(http(s)?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/.test(v) || 'Некорректный URL'
    // проверка на наличте протокола
    if (!/(http(s?)):\/\//i.test(v)) return 'Некорректный URL'
    // проверка на валиднасть ссылки: потокол + доменн/поддомен.зона + остальная часть url
    return /^http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/.test(v) || 'Некорректный URL'
  }

  const isGreatZero = (v: number) => {
    return v > 0 || 'Поле обязательно для заполнения'
  }

  const isEmail = (v: string | null) => {
    return !v || !v.length
      ? true
      : /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(v) || 'Некорректный email'
  }

  const isPhoneNumber = (v: string | null) => {
    return !v || !v.length
      ? true
      : /^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$/.test(v) ||
          'Некорректный номер телефона'
  }

  const isOnlyLetters = (v: string | null) => {
    return !v || !v.length
      ? true
      : /^[a-zA-Zа-яА-ЯёЁ\s\-.]+$/.test(v) ||
          'Строка может содержать только буквы, пробелы, тире и точки'
  }

  return {
    required,
    isUrl,
    isGreatZero,
    isEmail,
    isPhoneNumber,
    isOnlyLetters,
  }
}
