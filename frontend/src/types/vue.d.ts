import { Firestore } from 'firebase/firestore'
import { Database } from 'firebase/database'

import { ComponentCustomProperties } from 'vue'

export {}

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $fireDb: Database
    $fireStore: Firestore
  }
}
