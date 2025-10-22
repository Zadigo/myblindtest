import { Firestore } from 'firebase/firestore'
import { Database } from 'firebase/database'

export {}

// declare module '@vue/runtime-core' {
declare module 'vue' {
  interface ComponentCustomProperties {
    $fireDb: Database
    $fireStore: Firestore
  }
}
