import { toast } from 'vue-sonner'

/**
 * Hook called when the WebSocket is connected
 * @param ws WebSocket
 */
function onConnected(ws: WebSocket) {
  const sessionStore = useSessionStore()
  const { sessionId } = storeToRefs(sessionStore)

  const { stringify } = useWebsocketMessage()

  
  if (sessionStore.currentSettings) {
    const result = stringify({
      action: 'idle_connect',
      firebase_key: sessionId.value,
      session: sessionStore.currentSettings
    })

    ws.send(result)
    toast.success('Info', { description: 'Waiting for players' })
  }
}

/**
 * Hook called when the WebSocket is disconnected
 * @param store Store used for managing song state
 */
function onDisconnected(store: ReturnType<typeof useSongs>) {
  return () => {
    toast.error('Warning', {
      description: 'Game has been disconnected',
      unstyled: true,
      class: 'bg-yellow-100'
    })
    store.toggleGameStarted()
  }
}

/**
 * Hook called when the WebSocket encounters an error
 * @param store Store used for managing song state
 */
function onError(store: ReturnType<typeof useSongs>) {
  return () => {
    toast.error('Error', {
      description: 'An error has occured'
    })
    store.toggleGameStarted()
  }
}

/**
 * Composable used to a connect to the Django websocket
 * in order to start, stop etc. the blindtest game
 */
export function useGameWebsocket() {
  const songStore = useSongs()
  const { songsPlayed } = storeToRefs(songStore)

  const teamsStore = useTeamsStore()

  const wsObject = useWebSocket('ws://127.0.0.1:8000/ws/songs', {
    immediate: false,
    onConnected,
    onDisconnected: onDisconnected(songStore),
    onError: onError(songStore),
    onMessage(_ws, event: MessageEvent<string>) {
      const { parse } = useWebsocketMessage()
      const data = parse(event.data)

      if (data) {
        switch (data.action) {
          case 'idle_connect':
            if (data.code) {
              toast.success('Pin code', { description: `Pin code is ${data.code}` })
            }
            break

          case 'game_started':
            songStore.toggleGameStarted()
            break
            
          case 'song_new':
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

          case 'randomize_genre':
            if (data.song) songsPlayed.value.push(data.song)
            break
          
          case 'error':
            toast.error('Error', { description: `An error has occurred: ${data.message}` })
            break

          // Group actions

          case 'device_connected':
            toast.success('Device', { description: 'Projecton device pending connection' })
            break

          case 'device_disconnected':
            toast.warning('Device', { description: 'Projecton device disconnected' })
            break

          case 'device_accepted':
            toast.success('Device', { description: 'Projecton device accepted' })
            break

          default:
            console.warn('Unknown websocket action', data)
            break
        }
      }
    }
  })

  function startGame() {
    const { stringify } = useWebsocketMessage()
    const result = stringify({ action: 'start_game' })
    
    wsObject.send(result)
  }

  function stopGame(callback: () => void) {
    wsObject.close()
    callback()
  }

  const isConnected = computed(() => wsObject.status.value === 'OPEN')

  return {
    isConnected,
    /**
     * WebSocket object used to communicate with the server
     */
    wsObject,
    /**
     * Starts the blindtest
     */
    startGame,
    /**
     * Stops the blindtest
     */
    stopGame
  }
}
