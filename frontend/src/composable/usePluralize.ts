import { PluralForms } from '@/enums/pluralForms'

interface PluralizeComposition {
  pluralize: (count: number, titles: [string, string, string]) => string
  getPluralForms: (key: string) => [string, string, string]
}

export function usePluralize(): PluralizeComposition {
  function pluralize(count: number, titles: [string, string, string]): string {
    const cases = [2, 0, 1, 1, 1, 2]
    return titles[count % 100 > 4 && count % 100 < 20 ? 2 : cases[Math.min(count % 10, 5)]]
  }

  function getPluralForms(key: string): [string, string, string] {
    return [...(PluralForms[key as keyof typeof PluralForms] ?? [key, key, key])]
  }

  return {
    pluralize,
    getPluralForms,
  }
}
