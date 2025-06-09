import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createHead } from '@unhead/vue/client'
import { Icon } from '@iconify/vue'

import App from './App.vue'
import router from './routes'
import installPlugins from './plugins'

import 'animate.css'
import './style.scss'
import './assets/css/main.css'

const head = createHead()

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(head)
app.use(installPlugins())
app.component('VueIcon', Icon)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')
