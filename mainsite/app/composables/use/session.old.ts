export const _useSession = createGlobalState(() => {
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
        const baseDefaults = { ...defaultCacheOptions }
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

      const baseDefaults = { ...defaultCacheOptions }
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
