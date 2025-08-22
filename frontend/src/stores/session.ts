import { defaults } from '@/data/constants/cache'
import type { CacheSession } from '@/types'
import { addDoc, collection, deleteDoc, doc, updateDoc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'

/**
 * Store used to manage blindtest sessions
 */
export const useSessionStore = defineStore('session', () => {
  const fireStore = useFirestore()
  const sessionId = useSessionStorage<string>('sessionId', null)

  const hasExistingSession = computed(() => sessionId.value !== null)

  function createTeamIds(data: CacheSession) {
    // Generate the team IDs that will be used for 
    // the current session used for the current session
    const teamOne = data.teams.at(0)
    const teamTwo = data.teams.at(1)
  
    if (teamOne) {
      teamOne.id = generateRandomString(10).value
    }
  
    if (teamTwo) {
      teamTwo.id = generateRandomString(10).value
    }

    return data
  }

  /**
   * Creates a new session by saving the default settings
   * that we will be using for the blindtest to firebase
   */
  async function create() {
    if (!sessionId.value) {
      const collectionRef = collection(fireStore, 'blindtests')

      const baseDefaults = { ...defaults }
      const data = await addDoc(collectionRef, createTeamIds(baseDefaults))

      sessionId.value = data.id
    }
  }

  /**
   * Creates a brand new session in firebase
   */
  async function remove() {
    if (sessionId.value) {
      await deleteDoc(doc(fireStore, 'blindtests', sessionId.value))
      sessionId.value = null
    }
  }

  async function reset() {
    if (sessionId.value) {
      const collectionRef = collection(fireStore, 'blindtests')
      const docRef = doc(collectionRef, sessionId.value)

      const baseDefaults = { ...defaults }
      await updateDoc(docRef, createTeamIds(baseDefaults))
    }
  }

  const baseReturn = {
    /**
     * Creates a new session
     */
    create,
    /**
     * Remove an existing session
     */
    remove,
    /**
     * Resets an existing session.
     * @description The team IDs are modified
     */
    reset,
    hasExistingSession,
    sessionId
  }

  if (sessionId.value) {
    const currentSettings = useDocument<CacheSession>(doc(fireStore, 'blindtests', sessionId.value), { once: true })
  
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
      ...baseReturn,
      currentSettings
    }
  } else {
    return {
      ...baseReturn,
      currentSettings: null
    }
  }
})
