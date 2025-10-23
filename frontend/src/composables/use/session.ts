import type { CacheSession, Empty } from '@/types'
import { addDoc, collection, deleteDoc, doc, updateDoc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'

/**
 * Global state used to manage the current blindtest session
 */
export const useGlobalSessionState = createGlobalState(() => {
  const fireStore = useFirestore()
  const sessionId = useSessionStorage<string>('blindtestId', null)
  const docRef = doc(fireStore, 'blindtests', sessionId.value)
  const currentSettings = useDocument<CacheSession>(docRef, { once: true })

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
    sessionId,
    currentSettings
  }
})

/**
 * Composable used to manage blindtest sessions
 */
export const useSession = createSharedComposable(() => {
  const { sessionId } = useGlobalSessionState()
  const fireStore = useFirestore()

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

  async function create() {
    if (!sessionId.value) {
      const collectionRef = collection(fireStore, 'blindtests')

      const baseDefaults = { ...defaults }
      const data = await addDoc(collectionRef, createTeamIds(baseDefaults))

      sessionId.value = data.id
    }
  }

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

  onBeforeMount(async () => {
    if (!isDefined(sessionId)) {
      await create()
    }
  })

  return {
    sessionId,
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
     */
    reset,
    /**
     * Whether there is an existing session
     */
    hasExistingSession
  }
})
