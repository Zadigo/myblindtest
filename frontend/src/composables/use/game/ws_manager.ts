import { useSessionStore, useSongs } from '@/stores'
import { toast } from 'vue-sonner'

import type { WebsocketMessage, WebsocketInitializationMessage } from '@/types'

export function useWebsocketMessage() {
  function parse<T>(data: string): T | undefined {
    try {
      const parsedData = JSON.parse(data) as T
      return parsedData
    } catch (e) {
      console.error("Failed to parse websocket message", e)
      return undefined
    }
  }

  function send<T>(data: T): string {
    return JSON.stringify(data)
  }

  return {
    parse,
    send
  }
}

function onConnected(ws: WebSocket) {
  const sessionStore = useSessionStore()
  const { sessionId } = storeToRefs(sessionStore)
  const { send } = useWebsocketMessage()

  if (sessionStore.currentSettings) {
    const result = send<WebsocketInitializationMessage>({
      action: 'start_game',
      firebase_key: sessionId.value,
      session: sessionStore.currentSettings
    })

    ws.send(result)

    toast.success('Info', {
      description: 'Started blind test'
    })
  }
}

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

function onError(store: ReturnType<typeof useSongs>) {
  return () => {
    toast.error('Error', {
      description: 'An error has occured'
    })
    store.toggleGameStarted()
  }
}

function handleConnectionToken(data: WebsocketMessage) {
  // Handle the connection token message
  console.log(data)
}

/**
 * Composable used to a connect to the Django websocket
 * in order to start, stop etc. the blindtest game
 */
export function useGameWebsocket() {
  const songStore = useSongs()
  const { gameStarted, songsPlayed } = storeToRefs(songStore)

  const teamsStore = useTeamsStore()

  const wsObject = useWebSocket('ws://127.0.0.1:8000/ws/songs', {
    immediate: false,
    onConnected,
    onDisconnected: onDisconnected(songStore),
    onError: onError(songStore),
    onMessage(_ws, event: MessageEvent<string>) {
      const { parse } = useWebsocketMessage()
      const data = parse<WebsocketMessage>(event.data)

      if (data) {
        switch (data.action) {
          case 'connection_token':
            handleConnectionToken(data)
            break

          case 'game_started':
            songStore.toggleGameStarted()
            break

          case 'game_complete':
            break

          case 'song_new':
            if (data.song) songsPlayed.value.push(data.song)
            break

          case 'timer_tick':
            break

          case 'guess_correct':
            if (data.team_id && data.points) {
              const team = teamsStore.getTeam(data.team_id)
              if (team && team.value) {
                team.value.score += data.points
              }
            }
            break

          case 'song_skipped':
            break

          case 'randomize_genre':
            if (data.song) songsPlayed.value.push(data.song)
            break

          case 'device_connected':
            toast.success('Device', {
              description: 'Projecton device connected'
            })
            break

          case 'device_disconnected':
            toast.success('Device', {
              description: 'Projecton device disconnected'
            })
            break

          case 'error':
            gameStarted.value = false
            break

          default:
            break
        }
      }
    }
  })

  return {
    wsObject
  }
}
