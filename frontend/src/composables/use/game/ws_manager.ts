import type { BlindtestPlayer, CacheSession, Song, Undefineable } from '@/types'
import { promiseTimeout, set } from '@vueuse/core'
import { useSound } from '@vueuse/sound'
import { doc, updateDoc, arrayUnion } from 'firebase/firestore'
import { useToast } from 'primevue/usetoast'
import { useDocument, useFirestore } from 'vuefire'


export type WsSendMessage = { action: 'start_game' }
  | { action: 'stop_game' }
  | { action: 'not_guessed' }
  | { action: 'submit_guess', team_or_player_id: string, title_match: boolean, artist_match: boolean }
  | { action: 'game_settings', settings: Undefineable<CacheSession['settings']> }
  | { action: 'update_player', id: Undefineable<string>, name: string }

export type WsReceiveMessage = { action: 'device_accepted', player: BlindtestPlayer, players: Record<string, BlindtestPlayer> }
  | { action: 'device_disconnected', players: Record<string, BlindtestPlayer> }
  | { action: 'idle_connect', player: BlindtestPlayer }
  | { action: 'game_started' }
  | { action: 'song_new', song: Song }
  | { action: 'guess_correct', player_id: string, points: number, song: Song }
  | { action: 'guess_incorrect', player_id: string, points: number, song: Song }
  | { action: 'game_disconnected' }
  | { action: 'error', message: string }
  | { action: 'idle_response', code: number, connection_url: string }
  | { action: 'show_answer' }


/**
 * Websocket for individual game (admin)
 */
export const useGameWebsocketIndividual = createSharedComposable(() => {
  const toast = useToast()
  const { sessionId, currentSettings } = useSession()

  /**
   * Message
   */

  const { parse, stringify } = useWebsocketMessage()

  /**
   * Websocket
   */
  const fireStore = useFirestore()
  const docRef = doc(fireStore, 'blindtests', sessionId.value)
  
  const gameStarted = ref(false)

  const songStore = useSongs()
  const { songsPlayed } = storeToRefs(songStore)
  const { play } = useSound('tick.mp3')

  const wsObject = useWebSocket(`ws://127.0.0.1:8000/ws/songs/${sessionId.value}/single-player`, {
    immediate: false,
    onMessage: async (_ws, event: MessageEvent) => {
      const message = parse(event.data)

      if (isDefined(message)) {
        if (message.action === 'device_accepted') {
          play({  id: 1 })
          await updateDoc(docRef, { players: message.players })
          toast.add({ severity: 'info', summary: 'Device connected', detail: `Player ${message.player.id} has connected.`, life: 10000 })
        }

        if (message.action === 'device_disconnected') {
          play({ id: 2 })
          await updateDoc(docRef, { players: message.players })
          toast.add({ severity: 'warn', summary: 'Device disconnected', detail: `Player has disconnected.`, life: 3000 })
        }

        if (message.action === 'song_new') {
          if(message.song) {
            songsPlayed.value.push(message.song)
            songStore.incrementStep()
            await updateDoc(docRef, { songsPlayed: arrayUnion(message.song.id) } )
          }
        }

        if (message.action === 'idle_response') {
          const settings = stringify({ action: 'game_settings', settings: toValue(currentSettings)?.settings } )
          wsObject.send(settings)
        }

        if (message.action === 'error') {
          toast.add({ severity: 'error', summary: 'Error', detail: `Error from server: ${message.message}`, life: 10000 })
        }
      }
    },
    onDisconnected: (_ws, _event) => {
      toast.add({ severity: 'warn', summary: 'Disconnected', detail: 'WebSocket disconnected for individual game', life: 3000 })
    }
  })

  /**
   * State
   */

  const isConnected = computed(() => wsObject.status.value === 'OPEN')
  const blindTestDoc = useDocument(docRef)

  /**
   * Players
   */
  const players = computed(() => Object.keys(blindTestDoc.value?.players || []))
  

  return {
    gameStarted,
    wsObject,
    isConnected,
    blindTestDoc,
    players
  }
})

/**
 * Websocket for individual player (smartphone)
 */
export const useGameWebsocketIndividualPlayer = createSharedComposable(() => {
  const route = useRoute()
  
  const toast = useToast()
  const fireStore = useFirestore()
  const { parse } = useWebsocketMessage()

  const query = useUrlSearchParams('history')
  const playerId = useLocalStorage<string>('playerId', '')

  /**
   * Good answer states
   */

  const backgroundImage = refAutoReset<string>('/dancing1.jpg', 10000)
  const correctSong = refAutoReset<Song | null>(null, 10000)
  const isCorrectGuess = refAutoReset<boolean>(false, 10000)
  const isIncorrectGuess = refAutoReset<boolean>(false, 10000)
  const showAnswer = refAutoReset<boolean>(false, 10000)

  /**
   * Websocket
   */

  const wsObject = useWebSocket(`ws://127.0.0.1:8000/ws/single-player/${route.params.id}/connect`, {
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
      }

      if (message.action === 'game_started') {
        toast.add({ severity: 'info', summary: 'Game started', detail: 'The game has started!', life: 10000 })
      }

      if (message.action === 'guess_correct') {
        if (message.player_id === playerId.value) {
          const docRef = doc(fireStore, 'blindtests', route.params.id as string)
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
    }
  })

  /**
   * State
   */

  const isConnected = computed(() => wsObject.status.value === 'OPEN')

  const docRef = doc(fireStore, 'blindtests', route.params.id as string)
  const blindTestDoc = useDocument<CacheSession>(docRef)

  const players = computed(() => Object.keys(blindTestDoc.value?.players || {}))
  const player = computed(() => blindTestDoc.value?.players[playerId.value])

  const isReady = ref(false)

  tryOnMounted(async () => {
    await promiseTimeout(3000)
    set(isReady, true)
  })

  return {
    wsObject,
    isConnected,
    blindTestDoc,
    backgroundImage,
    isCorrectGuess,
    showAnswer,
    correctSong,
    isIncorrectGuess,
    isReady,
    players,
    player
  }
})

/**
 * Composable used to send game actions over websocket such as
 * starting/stopping the game, skipping songs, etc. -; this wraps
 * any websocket object and provides easy to use functions over it
 * @param wsObject The websocket object
 */
export function useGameActions (wsObject: ReturnType<typeof useWebSocket>, gameStarted: Ref<boolean>) {
  const { stringify } = useWebsocketMessage()

  function startGame() {
    const { stringify } = useWebsocketMessage()
    const result = stringify({ action: 'start_game' })

    wsObject.send(result)
    gameStarted.value = true
  }

  function stopGame(callback?: () => void) {
    gameStarted.value = false
    wsObject.send(stringify({ action: 'stop_game' }))
    wsObject.close()

    callback?.()
  }

  function sendIncorrectAnswer() {
    const result = stringify({ action: 'not_guessed' })

    if (result) {
      wsObject.send(result)
    }
  }

  const songsStore = useSongs()
  const { currentSong, correctAnswers, answers } = storeToRefs(songsStore)

  function sendCorrectAnswer(id: string, match: MatchedPart) {
    let title_match = true
    let artist_match = true

    if (match === 'Title') {
      title_match = true
      artist_match = false
    }

    if (match === 'Artist') {
      title_match = false
      artist_match = true
    }

    const result = stringify({
      action: 'submit_guess',
      team_or_player_id: id,
      title_match,
      artist_match
    })

    // console.log('handleCorrectAnswer', result)

    if (result) {
      wsObject.send(result)

      if (isDefined(currentSong)) {
        correctAnswers.value.push({
          playerId: id,
          matched: match,
          song: currentSong.value
        })

        answers.value.push({
          playerId: id,
          matched: match,
          song: currentSong.value
        })
      }
    }
  }

  return {
    /**
     * Starts the game
     * @param callback Optional callback to be called after starting the game
     */
    startGame,
    /**
     * Stops the game
     * @param callback Optional callback to be called after stopping the game
     */
    stopGame,
    /**
     * Sends a "not guessed" message over the websocket
     */
    sendCorrectAnswer,
    /**
     * Sends an incorrect answer message over the websocket
     */
    sendIncorrectAnswer
  }
}
