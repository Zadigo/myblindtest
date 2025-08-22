// import type { CacheSession } from '@/types'

// import { defaults } from '@/data/constants/cache'
import { addDoc, collection, doc, updateDoc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'

export const useSessionStore = defineStore('session', () => {
  const fireStore = useFirestore()
  const sessionId = useSessionStorage<string>('sessionId', null)

  const currentSettings = useDocument(doc(fireStore, 'blindtests', sessionId.value), { once: true })

  /**
   * Creates a new session by saving the default settings
   * that we will be using for the blindtest to firebase
   */
  async function create() {
    if (!sessionId.value) {
      const collectionRef = collection(fireStore, 'blindtests')
      const data = await addDoc(collectionRef, currentSettings.value)

      sessionId.value = data.id
    }
  }
  
  watchDebounced(currentSettings, async (newValue) => {
    if (sessionId.value) {
      const docRef = doc(fireStore, 'blindtests', sessionId.value)
      if (newValue) {
        await updateDoc(docRef, newValue)
      }
    }
  }, {
    debounce: 2000,
    deep: true
  })

  return {
    create,
    currentSettings,
    sessionId
  }
})
