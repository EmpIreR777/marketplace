import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'
import * as components from 'vuetify/components' // Import all components
import * as directives from 'vuetify/directives' // Import all directives
import { VTimePicker } from 'vuetify/labs/VTimePicker'
import { VDateInput } from 'vuetify/labs/VDateInput'
import { VNumberInput } from "vuetify/components/VNumberInput";
import { VFileUpload } from 'vuetify/labs/VFileUpload'
import { ru } from 'vuetify/locale'

const vuetify = createVuetify({
  locale: {
    locale: 'ru', // Устанавливаем русскую локаль
    messages: { ru }, // Передаём русскую локализацию
  },
  components: {
    ...components,
    VTimePicker,
    VDateInput,
    VNumberInput,
    VFileUpload,
  },
  directives,
  icons: {
    defaultSet: 'mdi', // Default icon set
    sets: {
      custom: {
        component: (props) => {
          const { icon } = props
          return {
            innerHTML: icon,
            style: { display: 'inline-flex', width: '24px', height: '24px' },
          }
        },
      },
    },
  },
})

export default vuetify
