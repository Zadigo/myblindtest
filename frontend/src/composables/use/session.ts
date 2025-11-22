import { addDoc, collection, deleteDoc, doc, updateDoc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'
import type { CacheSession } from '@/types'

/**
 * Generate the team IDs that will be used for
 * the current session used for the current session
 * @param data 
 * @returns 
 */
export function createTeamIds(data: CacheSession) {
  const teamOne = data.teams[0]
  const teamTwo = data.teams[1]

  if (teamOne) {
    teamOne.id = generateRandomString(10).value
  }

  if (teamTwo) {
    teamTwo.id = generateRandomString(10).value
  }

  return data
}

/**
 * Global state used to share the current session
 * across components in the application
 */
export const useSession = createGlobalState(() => {
  const fireStore = useFirestore()
  const sessionId = useSessionStorage<string>('blindtestId', null)

  /**
   * Initialize session
   */

  async function create() {
    if (!sessionId.value) {
      const collectionRef = collection(fireStore, 'blindtests')

      const baseDefaults = { ...defaults }
      const data = await addDoc(collectionRef, createTeamIds(baseDefaults))

      sessionId.value = data.id
    }
  }

  if (!isDefined(sessionId)) create()

  const docRef = doc(fireStore, 'blindtests', sessionId.value)
  const currentSettings = useDocument<CacheSession>(docRef)

  // Watch for changes and update the Firestore document
  watchDebounced(currentSettings, async (newValue) => {
    if (sessionId.value) {
      if (isDefined(newValue)) {
        await updateDoc(docRef, newValue)
      }
    }
  }, {
    debounce: 2000,
    deep: true
  })


  return {
    /**
     * Current session ID
     */
    sessionId,
    /**
     * Blindtest settings for the current session
     */
    currentSettings
  }
})

/**
 * Composable used to manage blindtest sessions
 */
export const useSessionManager = createSharedComposable(() => {
  const { sessionId } = useSession()
  const fireStore = useFirestore()

  const hasExistingSession = computed(() => sessionId.value !== null)

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

  return {
    sessionId,
    /**
     * Whether there is an existing session
     */
    hasExistingSession,
    /**
     * Remove an existing session
     */
    remove,
    /**
     * Resets an existing session.
     */
    reset,
  }
})
