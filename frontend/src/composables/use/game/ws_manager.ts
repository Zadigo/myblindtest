import { useToast } from 'primevue/usetoast'

/**
 * Hook called when the WebSocket is connected
 * @param ws WebSocket instance
 */
function onConnected(ws: WebSocket, toast: ReturnType<typeof useToast>) {
  const { currentSettings, sessionId } = useGlobalSessionState()
  const { stringify } = useWebsocketMessage()
  
  const result = stringify({
    action: 'idle_connect',
    firebase_key: sessionId.value,
    session: currentSettings.value
  })
  
  ws.send(result)

  toast.add({ severity: 'success', summary: 'Connection Established', detail: 'Waiting for players', life: 8000 })
  
  if (isDefined(currentSettings)) {
  }
}

/**
 * Hook called when the WebSocket is disconnected
 * @param store Store used for managing song state
 */
function onDisconnected(toast: ReturnType<typeof useToast>) {
  toast.add({ severity: 'warn', summary: 'Warning', detail: 'Game has been disconnected', life: 8000 })
}

/**
 * Hook called when the WebSocket encounters an error
 * @param store Store used for managing song state
 */
function onError(toast: ReturnType<typeof useToast>) {
  toast.add({ severity: 'error', summary: 'Error', detail: 'An error has occurred', life: 8000 })
}

/**
 * Shared composable used to a connect to the Django websocket
 * in order to start, stop etc. the blindtest game
 */
export const useGameWebsocket = createSharedComposable(() => {
  const songStore = useSongs()
  const { songsPlayed } = storeToRefs(songStore)
  const toast = useToast()
  const teamsStore = useTeamsStore()

  const [gameStarted, toggleGameStarted] = useToggle(false)

  const wsObject = useWebSocket('ws://127.0.0.1:8000/ws/songs', {
    immediate: false,
    onConnected: (ws) => onConnected(ws, toast),
    onDisconnected: () => onDisconnected(toast),
    onError: () => onError(toast),
    onMessage(_ws, event: MessageEvent<string>) {
      const { parse } = useWebsocketMessage()
      const data = parse(event.data)

      if (isDefined(data)) {
        switch (data.action) {
          case 'idle_response':
            if (data.code) {
              toast.add({ severity: 'info', summary: 'Pin code', detail: `Pin code is ${data.code}`, life: 50000 })
            }
            break

          case 'game_started':
            gameStarted.value = true
            break
            
          case 'song_new':
            console.log('New song received', data.song)
            if (data.song) songsPlayed.value.push(data.song)
            break

          case 'game_complete':
            break

          case 'guess_correct':
            if (data.team_id && data.points) {
              const team = teamsStore.getTeamById(ref(data.team_id))
              
              if (team.value) {
                team.value.score = data.points
              } else {
                console.error("Team not found in 'guess_correct'")
              }
            }
            break

          case 'timer_tick':
            break

          case 'song_skipped':
            break
          
          case 'error':
            console.error('WebSocket error received', data)
            toast.add({ severity: 'error', summary: 'Error', detail: `An error has occurred: ${data.message}`, life: 8000 })
            break

          // Group actions

          case 'device_accepted':
            toast.add({ severity: 'success', summary: 'Device', detail: 'Projecton device pending connection', life: 8000 })
            break

          case 'device_disconnected':
            toast.add({ severity: 'warn', summary: 'Device', detail: 'Projecton device disconnected', life: 8000 })
            break

          default:
            console.warn('Unknown websocket action', data)
            break
        }
      }
    }
  })

  /**
   * Actions
   */

  function startGame() {
    const { stringify } = useWebsocketMessage()
    const result = stringify({ action: 'start_game' })
    
    wsObject.send(result)
    gameStarted.value = true
  }

  function stopGame(callback: () => void) {
    gameStarted.value = false
    wsObject.close()
    if (isDefined(callback)) callback()
  }

  const isConnected = computed(() => wsObject.status.value === 'OPEN')

  const { stringify } = useWebsocketMessage()

  /**
   * Answering
   */

  const songsStore = useSongs()
  const { currentSong, correctAnswers, answers } = storeToRefs(songsStore)

  function handleFinalize() {
    songStore.incrementStep()
  }

  function sendIncorrectAnswer() {
    const result = stringify({ action: 'skip_song' })

    if (result) {
      wsObject.send(result)
      handleFinalize()
    }
  }

  function sendCorrectAnswer(teamId: string, match: MatchedPart) {
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
      team_id: teamId,
      title_match,
      artist_match
    })

    console.log('handleCorrectAnswer', result)

    if (result) {
      wsObject.send(result)

      if (isDefined(currentSong)) {
        correctAnswers.value.push({
          teamId: teamId,
          song: currentSong.value
        })

        answers.value.push({
          teamId: teamId,
          matched: match,
          song: currentSong.value
        })
      }

      console.log('BlindTestPage.handleCorrectAnswer', correctAnswers.value, answers.value)

      handleFinalize()
    }
  }

  return {
    isConnected,
    /**
     * WebSocket object used to communicate with the server
     */
    wsObject,
    /**
     * Whether the game was started
     * @default false
     */
    gameStarted,
    /**
     * Starts the blindtest
     */
    startGame,
    /**
     * Stops the blindtest
     */
    stopGame,
    /**
     * Sends an incorrect answer to the server
     * to skip the current song
     * @param team The team that answered incorrectly
     */
    sendIncorrectAnswer,
    /**
     * Sends a correct answer to the server
     * for the given team
     * @param teamId The ID of the team
     * @param match The element that was matched
     */
    sendCorrectAnswer,
    /**
     * Toggles the game started state
     */
    toggleGameStarted
  }
})
