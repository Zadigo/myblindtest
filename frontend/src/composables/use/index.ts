import type { CacheSession, GenreDistribution, SettingsApiResponse } from '@/types'
import { addDoc, collection, deleteDoc, doc, updateDoc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'

export * from './create'
export * from './game'
export * from './songs'

/**
 * Loads autocomplete data for the minimum and maximum time
 * period for the songs, the count by genre
 * 
 * @param fromCache Whether to load data from cache or fetch from API
 */
export const useLoadAutocompleteData = createSharedComposable((fromCache = false) => {
  const autocomplete = useLocalStorage<SettingsApiResponse>('autocomplete', null, {
    serializer: {
      write: (value) => JSON.stringify(value),
      read: (value) => (value ? JSON.parse(value) : null)
    }
  })

  onBeforeMount(async () => {
    if (!fromCache) {
      const { responseData } = await useAsyncRequest<SettingsApiResponse>('django', '/api/v1/songs/settings', { method: 'get', immediate: true })
      syncRef(autocomplete, responseData, { direction: 'rtl' })
    }
  })

  const minimumPeriod = computed(() => autocomplete.value?.period.minimum || 0)
  const maximumPeriod = computed(() => autocomplete.value?.period.maximum || 100)
  const genreDistribution = computed<GenreDistribution[]>(() => autocomplete.value?.count_by_genre || [])
  const genres = useArrayMap(genreDistribution, (item) => ({ label: item.genre, name: item.genre }))
  const genreNames = useArrayMap(genreDistribution, (item) => item.genre)

  return {
    /**
     * Autocomplete data for the songs settings
     */
    autocomplete,
    /**
     * Minimum period for the songs
     */
    minimumPeriod,
    /**
     * Maximum period for the songs
     */
    maximumPeriod,
    /**
     * Distribution of genres for the songs
     */
    genreDistribution,
    /**
     * List of genres for the songs
     */
    genres,
    /**
     * List of genre names for the songs
     */
    genreNames
  }
})

/**
 * Global state used to manage the current blindtest session
 */
export const useGlobalSessionState = createGlobalState(() => {
  const fireStore = useFirestore()
  const sessionId = useSessionStorage<string>('blindtestId', null)

  if (isDefined(sessionId)) {
    const currentSettings = useDocument<CacheSession>(doc(fireStore, 'blindtests', sessionId.value), { once: true })
    
    // Watch for changes and update the Firestore document
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

    console.log('Loaded session ID from global session state:', currentSettings.value)

    return {
      sessionId,
      currentSettings
    }
  } else {
    console.warn('No session ID found in global session state')
    return {
      sessionId,
      currentSettings: null
    }
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
