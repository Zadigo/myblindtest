import { initializeApp } from 'firebase/app'
import { getDatabase } from 'firebase/database'
import { getFirestore } from 'firebase/firestore'

import type { App } from 'vue'

const env = import.meta.env

export const firebaseApp = initializeApp({
  apiKey: env.VITE_FIREBASE_API_KEY,
  authDomain: env.VITE_FIREBASE_AUTH_DOMAIN,
  databaseURL: env.VITE_FIREBASE_DATABASE_URL,
  storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET,
  appId: env.VITE_FIREBASE_APP_ID,
  projectId: env.VITE_FIREBASE_PROJECT_ID,
  measurementId: env.VITE_FIREBASE_MEASUREMENT_ID,
  messagingSenderId: env.VITE_FIREBASE_MESSAGING_SENDER_ID
})

const db = getDatabase(firebaseApp)
const store = getFirestore(firebaseApp)

export function createFirebase(vueApp: App) {
  vueApp.config.globalProperties.$fireDb = db
  vueApp.config.globalProperties.$fireStore = store

  return {
    db,
    store
  }
}
