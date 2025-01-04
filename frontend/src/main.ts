import { createApp } from 'vue'
import { createPinia  } from 'pinia'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createHead } from 'unhead'
import { createVuetify } from 'vuetify'

import App from './App.vue'
import router from './routes'
import installPlugins from './plugins'

import './style.scss'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'mdb-ui-kit/css/mdb.min.css'

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import colors from 'vuetify/util/colors'
import { aliases, mdi } from 'vuetify/iconsets/mdi'


createHead()

const app = createApp(App)

const pinia = createPinia()

const vuetify = createVuetify({
    components,
    directives,
    date: {
        // adapter: DayJsAdapter
    },
    theme: {
        themes: {
            light: {
                dark: false,
                colors: {
                    primary: colors.red.darken1
                }
            }
        }
    },
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi
        }
    }
})

app.use(vuetify)
app.use(pinia)
app.use(router)
app.use(installPlugins())
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')
