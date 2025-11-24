/**
 * this websocket manager is used by the Admin (user who created the game) for
 * other players to join. It implements all the necessary message handling and state
 * management for the admin side of the game
 */

import { useSound } from '@vueuse/sound'
import { arrayUnion, doc, updateDoc } from 'firebase/firestore'
import { useToast } from 'primevue/usetoast'
import { useDocument, useFirestore } from 'vuefire'

/**
 * Websocket for individual game (admin)
 */
export const useAdminWebsocket = createSharedComposable(() => {
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
          play({ id: 1 })
          await updateDoc(docRef, { players: message.players })
          toast.add({ severity: 'info', summary: 'Device connected', detail: `Player ${message.player.id} has connected.`, life: 10000 })
        }

        if (message.action === 'device_disconnected') {
          play({ id: 2 })
          await updateDoc(docRef, { players: message.players })
          toast.add({ severity: 'warn', summary: 'Device disconnected', detail: `Player has disconnected.`, life: 3000 })
        }

        if (message.action === 'song_new') {
          if (message.song) {
            songsPlayed.value.push(message.song)
            songStore.incrementStep()
            await updateDoc(docRef, { songsPlayed: arrayUnion(message.song.id) })
          }
        }

        if (message.action === 'idle_response') {
          const settings = stringify({ action: 'game_settings', settings: toValue(currentSettings)?.settings })
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
 * Composable used to send game actions over websocket such as
 * starting/stopping the game, skipping songs, etc. -; this wraps
 * any websocket object and provides easy to use functions over it
 * @param wsObject The websocket object
 */
export function useGameActions(wsObject: ReturnType<typeof useWebSocket>, gameStarted: Ref<boolean>) {
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
