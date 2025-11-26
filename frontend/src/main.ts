import { Icon } from '@iconify/vue'
import { createHead } from '@unhead/vue/client'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createVueAxiosManager } from 'vue-axios-manager'
import { i18n } from './i18n'

import AnimateOnScroll from 'primevue/animateonscroll'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import App from './App.vue'
import installPlugins from './plugins'
import router from './router'

import 'animate.css'
import './style.css'

const app = createApp(App)

const head = createHead({
  init: [
    {
      title: '...',
      titleTemplate: '%s | Blindtest',
      htmlAttrs: { lang: 'en' }
    }
  ]
})

const axiosManager = createVueAxiosManager({
  disableAuth: true,
  endpoints: [
    {
      name: 'django',
      label: 'Django',
      dev: import.meta.env.VITE_DJANGO_PROD_DOMAIN,
      disableAuth: true
    }
  ]
})

app.use(createPinia())
app.use(i18n)
app.use(axiosManager)
app.use(router)
app.use(ToastService)
app.use(installPlugins())
app.use(PrimeVue, { unstyled: true })
app.use(head)
app.directive('animateonscroll', AnimateOnScroll)
app.component('VueIcon', Icon)
app.provide('google', () => {})
app.mount('#app')
