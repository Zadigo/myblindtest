/**
 * This websocket manager is used by the individual player (smartphone users)
 * who join a game hosted by an admin. It implements all the necessary message
 * handling and state management for the player side of the game.
 */

import type { CacheSession, Song } from '~/types'
import { promiseTimeout, set } from '@vueuse/core'
import { arrayUnion, doc, updateDoc } from 'firebase/firestore'
import { useToast } from 'primevue/usetoast'
import { useDocument, useFirestore } from 'vuefire'

/**
 * Websocket for individual player (smartphone)
 */
export const usePlayerWebsocket = createSharedComposable(() => {
  const router = useRouter()
  const route = useRoute()

  const toast = useToast()
  const fireStore = useFirestore()
  const { parse } = useWebsocketMessage()

  const query = useUrlSearchParams('history')
  const playerId = useLocalStorage<string>('playerId', '')

  /**
   * Answer states
   */

  const selected = ref<number | null>(null)
  const isAnswered = computed(() => selected.value !== null)

  /**
   * Good answer states
   */

  const backgroundImage = refAutoReset<string>('/dancing1.jpg', 10000)
  const correctSong = refAutoReset<Song | null>(null, 10000)
  const isCorrectGuess = refAutoReset<boolean>(false, 10000)
  const isIncorrectGuess = refAutoReset<boolean>(false, 10000)
  const showAnswer = refAutoReset<boolean>(false, 10000)

  /**
   * Start state
   */

  const isStarted = ref(false)
  
  const goToGamePage = useDebounceFn(() => {
    router.push(`/blindtest/player/game?game=${route.query.id}&player=${playerId.value}`)
  }, 2000)

  watchOnce(isStarted, async (newVal) => {
    if (newVal) {
      goToGamePage()
    }
  })

  // Indicates if the game was started before (to avoid re-navigation)
  // and in case of reconnection just automatically open the websocket
  // connection once again
  const wasStarted = useLocalStorage<boolean>('blindtestWasStarted', false)

  /**
   * Websocket
   */

  const wsObject = useWebSocket(`ws://127.0.0.1:8000/ws/single-player/${route.query.id}/connect`, {
    immediate: false,
    onConnected: async (_ws) => {
      toast.add({ severity: 'info', summary: 'Connected', detail: 'WebSocket connected for individual player', life: 3000 })
    },
    onDisconnected: (_ws, _event) => {
      toast.add({ severity: 'warn', summary: 'Disconnected', detail: 'WebSocket disconnected for individual player', life: 3000 })
    },
    onMessage: async (_ws, event: MessageEvent) => {
      const message = parse(event.data)

      if (!isDefined(message)) return

      if (message.action === 'idle_connect') {
        playerId.value = message.player.name
        query.player = playerId.value
        wasStarted.value = true
      }

      if (message.action === 'game_started') {
        isStarted.value = true
      }

      if (message.action === 'guess_correct') {
        if (message.player_id === playerId.value) {
          const docRef = doc(fireStore, 'blindtests', route.query.id as string)
          await updateDoc(docRef, {
            [`players.${playerId.value}.points`]: message.points,
            [`players.${playerId.value}.correctAnswers`]: arrayUnion(message.song.id)
          })

          isCorrectGuess.value = true
        }
      }

      if (message.action === 'guess_incorrect') {
        isIncorrectGuess.value = true
      }

      // Common for both correct and incorrect answers
      if (message.action === 'guess_correct' || message.action === 'guess_incorrect') {
        correctSong.value = message.song
        backgroundImage.value = message.song.artist.spotify_avatar
      }

      if (message.action === 'game_disconnected') {
        toast.add({ severity: 'warn', summary: 'Game disconnected', detail: 'The game has ended or the host has disconnected.', life: 10000 })
      }

      if (message.action === 'show_answer') {
        showAnswer.value = true
      }

      if (message.action === 'error') {
        toast.add({ severity: 'error', summary: 'Error', detail: `Error from server: ${message.message}`, life: 10000 })
      }

      if (message.action === 'game_paused') {
        toast.add({ severity: 'info', summary: 'Game paused', detail: 'The game has been paused by the host.', life: 10000 })
      }

      if (message.action === 'try_reconnection') {
        goToGamePage()
      }

      if (message.action === 'next_song_loaded') {
        selected.value = null
      }
    }
  })

  /**
   * State
   */

  const isConnected = computed(() => wsObject.status.value === 'OPEN')

  // This is a special way to connect to the Firebase database using the
  // ID provided by the url. Since the smartphone user and the admin operate
  // on two different sides, they need to have their own way of connecting
  // to the same document (or default game settings)
  const docRef = doc(fireStore, 'blindtests', route.query.id as string)
  const blindTestDoc = useDocument<CacheSession>(docRef)

  const players = computed(() => Object.keys(blindTestDoc.value?.players || {}))
  const player = computed(() => blindTestDoc.value?.players[playerId.value])

  const isReady = ref(false)

  tryOnMounted(async () => {
    await promiseTimeout(3000)
    set(isReady, true)

    // On mount, if the game was already started before,
    // and the player was disconnected, just reconnect automatically
    if (wasStarted.value && !isConnected.value) {
      wsObject.open()
    }
  })

  return {
    /**
     * Websocket
     */
    wsObject,
    /**
     * State
     * @default false
     */
    isConnected,
    /**
     * Firestore document for the blindtest session
     */
    blindTestDoc,
    /**
     * The image of the artist to show as 
     * background when a correct answer is given
     * @default '/dancing1.jpg'
     */
    backgroundImage,
    /**
     * Indicates if the last guess was correct
     * @default false
     */
    isCorrectGuess,
    /**
     * Indicates if the answer should be shown
     * @default false
     */
    showAnswer,
    /**
     * The song that was answered
     * @default null
     */
    correctSong,
    /**
     * Indicates if the last guess was incorrect
     * @default false
     */
    isIncorrectGuess,
    /**
     * Indicates if the player is ready
     * @default false
     */
    isReady,
    /**
     * List of players in the game
     * @default []
     */
    players,
    /**
     * The current player object
     * @default null
     */
    player,
    /**
     * The selected answer index
     * @default null
     */
    selected,
    /**
     * Indicates if the player has answered the current question
     * @default false
     */
    isAnswered,
    query
  }
})
