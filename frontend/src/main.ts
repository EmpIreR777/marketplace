import './scss/main.scss'
import vuetify from './plugins/vuetify';
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import VueApexCharts from 'vue3-apexcharts'

import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css';
import type {UserModule} from "@/types.ts";

const app = createApp(App)


app.use(createPinia())
app.use(router)
app.use(vuetify)
app.use(VueApexCharts)
// Install modules under `modules/`
Object.values(import.meta.glob<{ install: UserModule }>('./modules/*.ts', { eager: true }))
  .forEach(i => i.install?.({ app, router }))
app.mount('#app')
