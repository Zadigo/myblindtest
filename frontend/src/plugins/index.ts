import { createFirebase } from './firebase'

import { type App } from 'vue'

export * from './client'
export * from './date'
export * from './firebase'
export * from './client3'

import './fontawesome'

export default function installPlugins() {
  return {
    install(app: App) {
      createFirebase(app)
    }
  }
}
