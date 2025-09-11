import type { Recordable } from '@/types'

export function useFormData(data: Recordable): FormData {
  const formData = new FormData()

  const appendValue = (key: string, value: unknown) => {
    if (value === null || value === undefined) return

    if (Array.isArray(value)) {
      value.forEach((item) => {
        if (item instanceof File) {
          appendValue(key, item)
        } else {
          appendValue(key, item)
        }
      })
    } else if (value instanceof File) {
      formData.append(key, value)
    } else if (value instanceof Date) {
      formData.append(key, value.toISOString().split('T')[0])
    } else if (typeof value === 'boolean') {
      formData.append(key, value ? 'true' : 'false')
    } else if (typeof value === 'object') {
      Object.entries(value).forEach(([subKey, subValue]) =>
        appendValue(`${key}[${subKey}]`, subValue),
      )
    } else {
      formData.append(key, value.toString())
    }
  }

  Object.entries(data).forEach(([key, value]) => appendValue(key, value))

  return formData
}
