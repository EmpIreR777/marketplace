import type { IUniversitiesFilterCatalog } from '@/api/models'

export function useFormat() {
  const formatNumber = (value: number) => {
    return new Intl.NumberFormat('ru-RU').format(value)
  }

  function firstLetterLowerDot(str: string): string {
    if (!str) return ''
    return str[0].toLowerCase() + '.'
  }

  function formatUniversitiesCatalog(data: any) {
    return Object.fromEntries(
      Object.entries(data).map(([key, value]) => {
        if (value && typeof value === 'object' && 'items' in value) {
          const items = Object.entries(value.items as Record<string, string>).map(([id, name]) => ({
            id: Number(id),
            name,
          }))

          return [key, { ...value, items }]
        }

        return [key, value]
      }),
    ) as IUniversitiesFilterCatalog
  }

  return { formatNumber, firstLetterLowerDot, formatUniversitiesCatalog }
}
