import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createUnhead } from 'unhead'
import { Icon } from '@iconify/vue'

import App from './App.vue'
import router from './routes'
import installPlugins from './plugins'

import './style.scss'
import './assets/css/main.css'
// import './assets/spinners.scss'
import 'animate.css'

createUnhead()

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(installPlugins())
app.component('VueIcon', Icon)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')
