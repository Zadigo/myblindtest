import { Icon } from '@iconify/vue'
import { createHead } from '@unhead/vue/client'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVueAxiosManager } from 'vue-axios-manager'

import PrimeVue from 'primevue/config'
import installPlugins from './plugins'
import ToastService from 'primevue/toastservice'
import AnimateOnScroll from 'primevue/animateonscroll'
import App from './App.vue'
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
app.use(axiosManager)
app.use(router)
app.use(ToastService)
app.use(installPlugins())
app.use(PrimeVue, { unstyled: true })
app.use(head)
app.directive('animateonscroll', AnimateOnScroll)
app.component('VueIcon', Icon)

app.mount('#app')
