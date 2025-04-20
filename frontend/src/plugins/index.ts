import { type App } from 'vue'
import { installAxiosClient } from './client'
import { createFirebase } from './firebase'

export * from './client'
export * from './date'
export * from './firebase'

import './fontawesome'

export default function installPlugins() {
  return {
    install(app: App) {
      installAxiosClient(app)
      createFirebase(app)
    }
  }
}
