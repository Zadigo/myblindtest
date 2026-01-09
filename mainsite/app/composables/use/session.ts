import { promiseTimeout } from '@vueuse/core'
import { addDoc, collection, deleteDoc, doc, setDoc, updateDoc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'
import { defaultCacheOptions } from '~/data'
import type { CacheSession, Empty } from '~/types'


export function useCreateSession() {
  if (import.meta.server) {
    return {
      create: async () => { }
    }
  }

  const fireStore = useFirestore()
  const sessionId = useSessionStorage<string>('blindtestId', null)

  async function create() {
    if (!isDefined(sessionId)) {
      try {
        const collectionRef = collection(fireStore, 'blindtests')
        const data = await addDoc(collectionRef, { ...defaultCacheOptions })
        await promiseTimeout(800) // Wait a bit to ensure Firestore is ready

        sessionId.value = data.id
      } catch (error) {
        throw new Error('Error creating blindtest session:' + error)
      }
    }
  }

  return {
    create
  }
}

/**
 * This composable manages the blindtest session. It handles creating,
 * retrieving, updating, and deleting the session data in Firestore. A session
 * can be considered as a game instance where players can join and participate
 * in a blindtest
 */
export const useSession = createGlobalState(() => {
  const currentSettings = ref<Empty<CacheSession>>()

  if (import.meta.server) {
    return {
      docRef: null,
      sessionId: null,
      currentSettings,
      hasExistingSession: ref(false),
      reset: async () => { },
      remove: async () => { },
      // create: async () => { }
    }
  }
  
  const sessionId = useSessionStorage<string>('blindtestId', null)
  const hasExistingSession = computed(() => isDefined(sessionId))

  // If there is an ID in the route, use that as session ID

  const route = useRoute()
  if (route.params.id && typeof route.params.id === 'string') {
    sessionId.value = route.params.id
  }

  // Key in local storage but not on Firebase. If there's
  // no document just clear the local storage

  const fireStore = useFirestore()

  if (!isDefined(sessionId)) {
    console.info('❌ Call useCreateSession() before using the session')
    return {
      docRef: null,
      sessionId: null,
      currentSettings,
      hasExistingSession: ref(false),
      reset: async () => { },
      remove: async () => { },
      // create: async () => { }
    }
  }

  const docRef = doc(fireStore, 'blindtests', sessionId.value)
  const _currentSettings = useDocument<CacheSession>(docRef)

  tryOnMounted(() => { currentSettings.value = _currentSettings.value })

  watchDebounced(currentSettings, async (newValue) => {
    if (isDefined(docRef) && isDefined(sessionId)) {
      try {
        if (isDefined(newValue)) {
          await setDoc(docRef, newValue, { merge: true })
        }
      } catch (e) {
        console.error('Error updating session settings:', e)
      }
    }
  }, { debounce: 1000, deep: true, immediate: false })

  async function reset() {
    if (isDefined(sessionId)) {
      await updateDoc(docRef, { ...defaultCacheOptions  })
    }
  }

  async function remove() {
    if (isDefined(sessionId)) {
      await deleteDoc(docRef)
      sessionId.value = null
    }
  }

  return {
    docRef,
    /**
     * Current session ID
     */
    sessionId: readonly(sessionId),
    /**
     * Blindtest settings for the current session
     */
    currentSettings,
    /**
     * Whether there is an existing session
     */
    hasExistingSession,
    /**
     * Resets an existing session.
     */
    reset,
    /**
     * Remove an existing session
     */
    remove,
    // create
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

/**
 * This composable is used to get the songs played
 * in the current blindtest session
 */
// export const useSongsPlayedSession = createGlobalState(() => {
//   const fireStore = useFirestore()
//   const sessionId = useSessionStorage<string>('blindtestId', null)

//   if (!isDefined(sessionId)) {
//     return {
//       docRef: null
//     }
//   }

//   const songsPlayed = ref<Song[]>([])
//   const docRef = doc(fireStore, 'blindtests', sessionId.value)
//   const _songsPlayed = useDocument<Song[]>(docRef)

//   watch(_songsPlayed, (newValue) => {
//     if (isDefined(newValue)) {
//       songsPlayed.value = songsPlayed.value || []
//     }
//   }, {
//     immediate: true,
//     deep: true
//   })

//   watchDebounced(songsPlayed, async (newValue) => {
//     if (isDefined(newValue) && isDefined(sessionId)) {
//       await updateDoc(docRef, {
//         songsPlayed: newValue
//       })
//     }
//   }, {
//     debounce: 1000,
//     deep: true
//   })

//   return {
//     docRef
//   }
// })
