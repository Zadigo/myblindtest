import type { CacheSession } from '@/types'
import { promiseTimeout } from '@vueuse/core'
import { addDoc, collection, deleteDoc, doc, getDoc, updateDoc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'

/**
 * This composable manages the blindtest session. It handles creating,
 * retrieving, updating, and deleting the session data in Firestore. A session
 * can be considered as a game instance where players can join and participate
 * in a blindtest
 */
export const useSession = createGlobalState(() => {
  const fireStore = useFirestore()
  const sessionId = useSessionStorage<string>('blindtestId', null)

  /**
   * Key in url
   * @description If there is an ID in the route, use that as session ID
   */

  const route = useRoute()

  if (route.params.id && typeof route.params.id === 'string') {
    sessionId.value = route.params.id
  }

  /**
   * Key in local storage but not on Firebase
   */
  
  if (isDefined(sessionId)) {
    const docRef = doc(fireStore, 'blindtests', sessionId.value)

    getDoc(docRef).then((docSnap) => {
      if (!docSnap.exists()) {
        sessionId.value = null
      }
    })
  }

  /**
   * Initialize session
   */

  async function create() {
    if (!isDefined(sessionId)) {
      const collectionRef = collection(fireStore, 'blindtests')

      try {
        const baseDefaults = { ...defaults }
        const data = await addDoc(collectionRef, baseDefaults)
        sessionId.value = data.id
      } catch (error) {
        console.error('Error creating blindtest session:', error)
        return
      }
    }

    // Wait a bit to ensure Firestore is ready and
    // ensure that the document can be accessed
    await promiseTimeout(1000)
  }
  
  create()

  const docRef = doc(fireStore, 'blindtests', sessionId.value)
  const currentSettings = useDocument<CacheSession>(docRef)

  // TODO: Transform into a writable computed property
  // Watch for changes and update the Firestore document
  watchDebounced(currentSettings, async (newValue) => {
    if (sessionId.value) {
      if (isDefined(newValue)) {
        await updateDoc(docRef, newValue)

        if (newValue.settings.soloMode) {
          newValue.players['admin'] = {
            id: 'admin',
            name: 'Admin',
            points: 0,
            color: '#FF0000',
            correctAnswers: [],
            team: null,
            position: 1,
            speciality: null
          }
        } else {
          delete newValue.players['admin']
        }
      }
    }
  }, {
    debounce: 2000,
    deep: true
  })

  /**
   * Actions
   */

  const hasExistingSession = computed(() => sessionId.value !== null)

  async function remove() {
    if (sessionId.value) {
      await deleteDoc(doc(fireStore, 'blindtests', sessionId.value))
      sessionId.value = null
    }
  }

  const sonsStore = useSongs()

  async function reset() {
    if (sessionId.value) {
      const collectionRef = collection(fireStore, 'blindtests')
      const docRef = doc(collectionRef, sessionId.value)

      const baseDefaults = { ...defaults }
      await updateDoc(docRef, baseDefaults)

      sonsStore.reset()
    }
  }

  return {
    /**
     * Current session ID
     */
    sessionId,
    /**
     * Blindtest settings for the current session
     */
    currentSettings,
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
    reset
  }
})

/**
 * This composable is used to manage the player session state
 * across the application. It takes the firebase session ID
 * directly from the current url
 * 
 */
export const usePlayerSession = createGlobalState(() => {
  const fireStore = useFirestore()
  const route = useRoute()

  const docRef = doc(fireStore, 'blindtests', route.params.id as string)
  const currentSettings = useDocument<CacheSession>(docRef)

  return {
    currentSettings
  }
})
