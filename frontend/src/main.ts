import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createHead } from '@unhead/vue/client'
import { Icon } from '@iconify/vue'
import { createVueAxiosManager } from './plugins/client3'

import App from './App.vue'
import router from './routes'
import installPlugins from './plugins'
import PrimeVue from 'primevue/config'
import AnimateOnScroll from 'primevue/animateonscroll'

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
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')
