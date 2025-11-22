import type { CacheSession, IndividualBlindTestPlayer, Song } from '@/types'
import { doc, updateDoc } from 'firebase/firestore'
import { useToast } from 'primevue/usetoast'
import { useDocument, useFirestore } from 'vuefire'


export type SendIndividualBlindTestMessage = { action: 'start_game' }
  | { action: 'stop_game' }
  | { action: 'skip_song' }
  | { action: 'submit_guess', team_or_player_id: string, title_match: boolean, artist_match: boolean }

export type ReceiveIndividualBlindTestMessage = { action: 'device_accepted', players: Record<string, IndividualBlindTestPlayer> }
  | { action: 'device_disconnected', players: Record<string, IndividualBlindTestPlayer> }
  | { action: 'idle_connect', session_id: string, player: IndividualBlindTestPlayer }
  | { action: 'game_started' }
  | { action: 'song_new', song: Song }
  | { action: 'guess_correct', player_id: string, points: number, song: Song }
  | { action: 'guess_incorrect', player_id: string, points: number, song: Song }
  | { action: 'game_disconnected' }


/**
 * Websocket for individual game (admin)
 */
export const useGameWebsocketIndividual = createSharedComposable(() => {
  const { sessionId } = useSession()

  /**
   * Message
   */

  const { parse } = useWebsocketMessage<SendIndividualBlindTestMessage, ReceiveIndividualBlindTestMessage>()

  /**
   * Websocket
   */
  const toast = useToast()
  const fireStore = useFirestore()
  const docRef = doc(fireStore, 'blindtests', sessionId.value)
  const gameStarted = ref(false)

  const songStore = useSongs()
  const { songsPlayed } = storeToRefs(songStore)

  const wsObject = useWebSocket(`ws://127.0.0.1:8000/ws/songs/${sessionId.value}/single-player`, {
    immediate: false,
    onMessage: async (_ws, event: MessageEvent) => {
      const message = parse(event.data)

      if (isDefined(message)) {
        if (message.action === 'device_accepted') {
          await updateDoc(docRef, { players: message.players })
          toast.add({ severity: 'info', summary: 'Device connected', detail: `Player has connected.`, life: 3000 })
        }

        if (message.action === 'device_disconnected') {
          await updateDoc(docRef, { players: message.players })
          toast.add({ severity: 'warn', summary: 'Device disconnected', detail: `Player has disconnected.`, life: 3000 })
        }

        if (message.action === 'song_new') {
          if(message.song) songsPlayed.value.push(message.song)
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

  /**
   * Websocket
   */
  const toast = useToast()
  const fireStore = useFirestore()
  const { parse } = useWebsocketMessage<SendIndividualBlindTestMessage, ReceiveIndividualBlindTestMessage>()

  const playerId = useLocalStorage<string>('playerId', '')

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
      }

      if (message.action === 'game_started') {
        toast.add({ severity: 'info', summary: 'Game started', detail: 'The game has started!', life: 10000 })
      }

      if (message.action === 'guess_correct') {
        if (message.player_id === playerId.value) {
          const docRef = doc(fireStore, 'blindtests', route.params.id as string)
          await updateDoc(docRef, { [`players.${playerId.value}.points`]: message.points })
        }
      }

      if (message.action === 'guess_incorrect') {
        // Do something on incorrect guess if needed
      }

      if (message.action === 'game_disconnected') {
        toast.add({ severity: 'warn', summary: 'Game disconnected', detail: 'The game has ended or the host has disconnected.', life: 10000 })
      }
    }
  })

  /**
   * State
   */

  const isConnected = computed(() => wsObject.status.value === 'OPEN')

  const docRef = doc(fireStore, 'blindtests', route.params.id as string)
  const blindTestDoc = useDocument<CacheSession>(docRef)

  const players = computed(() => blindTestDoc.value?.players)
  const player = computed(() => isDefined(players) ? players.value[playerId.value] : undefined)

  console.log('player', player.value)
  console.log('players', players.value)
  console.log('playerId', playerId.value)

  return {
    wsObject,
    isConnected,
    blindTestDoc,
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
  const { stringify } = useWebsocketMessage<SendIndividualBlindTestMessage, ReceiveIndividualBlindTestMessage>()

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

  const songStore = useSongs()

  function sendIncorrectAnswer() {
    const result = stringify({ action: 'skip_song' })

    if (result) {
      wsObject.send(result)
      songStore.incrementStep()
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
          teamId: id,
          song: currentSong.value
        })

        answers.value.push({
          teamId: id,
          matched: match,
          song: currentSong.value
        })
      }

      songStore.incrementStep()
    }
  }

  return {
    startGame,
    stopGame,
    sendCorrectAnswer,
    sendIncorrectAnswer
  }
}
