import { addDoc, collection, deleteDoc, doc, updateDoc, getDoc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'
import type { CacheSession } from '@/types'

/**
 * Global state used to share the current session
 * across components in the application
 */
export const useSession = createGlobalState(() => {
  const fireStore = useFirestore()
  const sessionId = useSessionStorage<string>('blindtestId', null)

  /**
   * Key in url
   */

  const route = useRoute()

  // If there is an ID in the route, use that as session ID
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
        // window.location.reload()
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
  }

  create()

  const docRef = doc(fireStore, 'blindtests', sessionId.value)
  const currentSettings = useDocument<CacheSession>(docRef)

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
            correct_answers: [],
            team: null
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

  async function reset() {
    if (sessionId.value) {
      const collectionRef = collection(fireStore, 'blindtests')
      const docRef = doc(collectionRef, sessionId.value)

      const baseDefaults = { ...defaults }
      await updateDoc(docRef, baseDefaults)
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
