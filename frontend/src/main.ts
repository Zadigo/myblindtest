import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createHead } from '@unhead/vue/client'
import { Icon } from '@iconify/vue'

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

app.use(pinia)
app.use(router)
app.use(head)
app.use(installPlugins())
app.use(PrimeVue, { unstyled: true })
app.directive('animateonscroll', AnimateOnScroll)
app.component('VueIcon', Icon)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')
