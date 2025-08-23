import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { usePlugins } from './plugins'
import { Icon } from '@iconify/vue'

import PrimeVue from 'primevue/config'
import App from './App.vue'

import './style.css'

const app = createApp(App)
const pinia = createPinia()

usePlugins()

app.use(pinia)
app.component('VueIcon', Icon)
app.use(PrimeVue, { unstyled: true })
app.mount('#app')
