import type { Plugin } from 'vue'
import { VueFire, VueFireAuth } from 'vuefire'
import { createFirebase, firebaseApp } from './firebase'

import { type App } from 'vue'

export * from './date'
export * from './firebase'

export default function installPlugins(): Plugin {
  return {
    install(app: App) {
      createFirebase(app)

      app.use(VueFire, {
        firebaseApp,
        modules: [
          VueFireAuth()
        ]
      })
    }
  }
}
