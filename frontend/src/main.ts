import { Icon } from '@iconify/vue'
import { createHead } from '@unhead/vue/client'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createVueAxiosManager } from 'vue-axios-manager'


import AnimateOnScroll from 'primevue/animateonscroll'
import PrimeVue from 'primevue/config'
import App from './App.vue'
import installPlugins from './plugins'
import router from './routes'

import 'animate.css'
import './style.css'

const head = createHead({
  init: [
    {
      title: '...',
      titleTemplate: '%s | Blindtest',
      htmlAttrs: { lang: 'en' }
    }
  ]
})

const app = createApp(App)
const pinia = createPinia()

const axiosManager = createVueAxiosManager({
  disableAuth: true,
  endpoints: [
    {
      name: 'django',
      label: 'Django',
      dev: import.meta.env.VITE_DJANGO_PROD_URL
    }
  ]
})

app.use(axiosManager)
app.use(pinia)
app.use(router)
app.use(head)
app.use(installPlugins())
app.use(PrimeVue, { unstyled: true })
app.directive('animateonscroll', AnimateOnScroll)
app.component('VueIcon', Icon)
app.mount('#app')
