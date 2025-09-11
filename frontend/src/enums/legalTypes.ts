import { AuthorTypeEnum } from '@/enums/userEnum'

export enum EntityType {
  INDIVIDUAL = 'individual',
  LEGAL = 'legal',
}

export enum LegalForm {
  FIZ = 'FIZ',
  FOP = 'FOP',
  LLC = 'LLC',
}

export const LegalFormTitle = {
  [LegalForm.FIZ]: 'Физ.лицо',
  [LegalForm.FOP]: 'Ип',
  [LegalForm.LLC]: 'ООО',
} as const

export const ApiLegalForm = {
  [LegalForm.FIZ]: AuthorTypeEnum.INDIVIDUAL,
  [LegalForm.FOP]: AuthorTypeEnum.INDIVIDUAL_ENTREPRENEUR,
  [LegalForm.LLC]: AuthorTypeEnum.ORGANIZATION,
}
