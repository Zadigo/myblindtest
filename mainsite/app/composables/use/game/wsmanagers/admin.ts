/**
 * this websocket manager is used by the Admin (user who created the game) for
 * other players to join. It implements all the necessary message handling and state
 * management for the admin side of the game
 */

import type { Undefineable, VueUseWsReturnType } from '~/types'
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

  /**
   * Player Answers
   */

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

            if (isDefined(currentSettings) && currentSettings.value.settings.multipleChoiceAnswers) {
              currentSettings.value.playerAnswers = []
              
              // When loading a new song, if there are pending score updates,
              // apply them to the players
              if (isDefined(currentSettings.value.pendingScoresUpdate)) {
                currentSettings.value.playerAnswers = []

                Object.keys(currentSettings.value.pendingScoresUpdate).forEach((playerId) => {
                  const playerValue = currentSettings.value.players[playerId]
                  if (isDefined(playerValue)) {
                    playerValue.points = currentSettings.value.pendingScoresUpdate[playerId]?.points || playerValue.points
                  }
                })
              }
            }
          }
        }

        if (message.action === 'idle_response') {
          const settings = stringify({ action: 'game_settings', settings: toValue(currentSettings)?.settings })
          wsObject.send(settings)
        }

        if (message.action === 'error') {
          toast.add({ severity: 'error', summary: 'Error', detail: `Error from server: ${message.message}`, life: 10000 })
        }

        if (message.action === 'update_possibilities') {
          if (isDefined(currentSettings)) {
            console.log('Updating possibilities for multiple choice answers:', message.choices)
            currentSettings.value.availableAnswers = message.choices
          }
        }

        if (message.action === 'player_submitted_answer') {
          console.log(`Player ${message.player_id} submitted answer index ${message.answer_index}`)

          await updateDoc(docRef, { playerAnswers: arrayUnion({ player_id: message.player_id, answer_index: message.answer_index }) })
        }

        if (message.action === 'multi_choice_updated_scores') {
          // Do not update the doc immediately. We will update it
          // when the admin loads the next song
          console.log('Received updated scores for multiple choice:', message.players)
          await updateDoc(docRef, { pendingScoresUpdate: message.players })
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
    /**
     * Whether the game has started
     * @default false
     */
    gameStarted,
    /**
     * Websocket object for the admin game
     */
    wsObject,
    /**
     * Whether the websocket is connected
     * @default false
     */
    isConnected,
    /**
     * Blind test document from Firestore
     */
    blindTestDoc,
    /**
     * List of players in the game
     * @default []
     */
    players
  }
})

/**
 * Wrapper for the base websocket that implemnts admin actions for the game
 * such as starting/stopping the game, sending correct/incorrect answers, etc.
 * @param wsObject The websocket object
 */
export function useGameActions(wsObject: VueUseWsReturnType, gameStarted: Ref<boolean>) {
  const { stringify } = useWebsocketMessage()

  function _startGame() {
    const { stringify } = useWebsocketMessage()
    const result = stringify({ action: 'start_game' })

    wsObject.send(result)
    gameStarted.value = true
  }

  function _pauseGame() {
    wsObject.send(stringify({ action: 'pause_game' }))
  }

  const toast = useToast()
  const songsStore = useSongs()
  const { currentSong, answers, correctAnswers } = storeToRefs(songsStore)

  function _stopGame(callback?: () => void) {
    gameStarted.value = false
    wsObject.send(stringify({ action: 'stop_game' }))
    wsObject.close()

    correctAnswers.value = []

    songsStore.songsPlayed = []
    songsStore.resetStep()
    toast.add({ severity: 'info', summary: 'Game Stopped', detail: 'The game has been successfully stopped and reset.', life: 8000 })

    callback?.()
  }

  function _sendIncorrectAnswer() {
    const result = stringify({ action: 'not_guessed' })

    if (result) {
      wsObject.send(result)
    }
  }

  function _sendCorrectAnswer(id: string, match: MatchedPart) {
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

  function _reconnectPlayer(playerId: Undefineable<string>) {
    wsObject.send(stringify({ action: 'reconnect_player', player_id: playerId }))
  }
  
  return {
    /**
     * Pauses the game
     * @param callback Optional callback to be called after pausing the game
     */
    pauseGame: useThrottleFn(_pauseGame, 3000),
    /**
     * Starts the game
     * @param callback Optional callback to be called after starting the game
     */
    startGame: useThrottleFn(_startGame, 3000),
    /**
     * Stops the game
     * @param callback Optional callback to be called after stopping the game
     */
    stopGame: useThrottleFn(_stopGame, 3000),
    /**
     * Sends a "not guessed" message over the websocket
     */
    sendCorrectAnswer: useThrottleFn(_sendCorrectAnswer, 500),
    /**
     * Sends an incorrect answer message over the websocket
     */
    sendIncorrectAnswer: useThrottleFn(_sendIncorrectAnswer, 500),
    /**
     * Attempts to reconnect a player by their ID
     * @param playerId The ID of the player to reconnect
     */
    reconnectPlayer: useThrottleFn(_reconnectPlayer, 5000)
  }
}

export function useMultiChoiceGameActions(wsObject: VueUseWsReturnType) {
  const {  currentSettings } = useSession()
  const { isActive, remaining } = useCountdown(3, { immediate: false })

  const { stringify } = useWebsocketMessage()

  function resetContainers() {
    if (isDefined(currentSettings)) {
      currentSettings.value.pendingScoresUpdate = {}
      currentSettings.value.availableAnswers = []
      currentSettings.value.playerAnswers = []
    }
  }

  async function _updateAnswersWithCountdown() {
    if (isDefined(currentSettings)) {
      currentSettings.value.players = currentSettings.value.pendingScoresUpdate
      wsObject.send(stringify({ action: 'next_song' }))
      resetContainers()
    }
  }

  tryOnBeforeUnmount(( ) => {
    resetContainers()
  })

  return {
    countDownActive: isActive,
    remaining,
    updateAnswersWithCountdown: useThrottleFn(_updateAnswersWithCountdown, 500)
  }

}
