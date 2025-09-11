import type { Recordable } from '@/types'

function isEqual(value1: unknown, value2: unknown): boolean {
  if (value1 === value2) return true

  if (value1 == null || value2 == null) return value1 === value2

  if (value1 instanceof Date && value2 instanceof Date) {
    return value1.getTime() === value2.getTime()
  }

  if (value1 instanceof File && value2 instanceof File) {
    return value1.name === value2.name && value1.size === value2.size && value1.type === value2.type
  }

  if (Array.isArray(value1) && Array.isArray(value2)) {
    return (
      value1.length === value2.length && value1.every((val, index) => isEqual(val, value2[index]))
    )
  }

  return false
}

export function useChangedFields<T extends Recordable>(original: T, updated: T): Partial<T> {
  const changedFields: Partial<T> = {}

  for (const key in updated) {
    const value = updated[key]

    if (value !== undefined) {
      const originalValue = original[key]

      if (Array.isArray(value) && Array.isArray(originalValue)) {
        if (!isEqual(value, originalValue)) {
          changedFields[key] = value
        }
      } else if (!isEqual(value, originalValue)) {
        changedFields[key] = value
      }
    }
  }

  return changedFields
}
