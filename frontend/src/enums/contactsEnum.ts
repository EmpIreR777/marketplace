import type { IInfoItem } from '@/types/index'
import {
  mapPinIcon,
  clockHour5Icon,
  phoneIcon,
  mailIcon,
  worldwwwIcon,
  telegramIcon,
  whatsappIcon,
} from '@/assets/icons'

export const linkType = {
  address: 'address',
  phone: 'phone',
  email: 'email',
  web: 'web',
  skype: 'skype',
  telegram: 'telegram',
  whatsapp: 'whatsapp',
} as const

export const NAME: IInfoItem = {
  icon: 'mdi-text-box-outline',
  title: 'Название',
  text: 'ООО «Эдикс»\nОГРН: 1254700002347\nИНН: 4706086286',
}

export const OGRN: IInfoItem = {
  icon: 'mdi-text-box-outline',
  title: 'ОГРН',
  text: '1254700002347',
}

export const INN: IInfoItem = {
  icon: 'mdi-text-box-outline',
  title: 'ИНН',
  text: '4706086286',
}

export const ADDRESS: IInfoItem = {
  imgSrc: mapPinIcon,
  title: 'Адрес',
  text: '188347, Ленинградская область, Всеволожский м. р-н, Всеволожское г. п., Всеволожск г., Пушкинская улица, д. 1а.',
  linkType: linkType.address,
}

export const WORK_SCHEDULE: IInfoItem = {
  imgSrc: clockHour5Icon,
  title: 'График работы',
  text: 'Пн-Пт: 9:00-18:00',
}

export const PHONE: IInfoItem = {
  imgSrc: phoneIcon,
  title: 'Телефон',
  text: '',
  linkType: linkType.phone,
}

export const MAIL: IInfoItem = {
  imgSrc: mailIcon,
  title: 'Электронная почта',
  text: 'Info@edx.ru',
  linkType: linkType.email,
}

export const WEBSITE: IInfoItem = {
  imgSrc: worldwwwIcon,
  title: 'Веб-сайт',
  text: 'https://EDX.ru',
  linkType: linkType.web,
}

export const TELEGRAM: IInfoItem = {
  imgSrc: telegramIcon,
  title: 'Telegram',
  text: '',
  linkType: linkType.telegram,
}

export const WHATSAPP: IInfoItem = {
  imgSrc: whatsappIcon,
  title: 'WhatsApp',
  text: '',
  linkType: linkType.whatsapp,
}

export const organizationInfoItems = [ADDRESS, WORK_SCHEDULE, PHONE]

export const organizationContactItems = [MAIL, WEBSITE, TELEGRAM, WHATSAPP]
