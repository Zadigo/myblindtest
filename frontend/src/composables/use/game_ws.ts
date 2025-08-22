import { useSessionStore } from '@/stores/session'
import { toast } from 'vue-sonner'

import type { WebsocketBlindTestMessage, WebsocketSettings } from '@/types'

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
  const { send } = useWebsocketMessage()

  if (sessionStore.currentSettings) {
    const result = send<WebsocketSettings>({
      action: 'start_game',
      cache: sessionStore.currentSettings
    })

    ws.send(result)
  }
}

function onDisconnected(ws: WebSocket) {
  // Handle disconnection
}

function onError(ws: WebSocket) {
  // Handle error
}

function handleConnectionToken(data: WebsocketBlindTestMessage) {
  // Handle the connection token message
}

function handleGameStarted(data: WebsocketBlindTestMessage) {
  // Handle the game started message
}

function handleSongNew(data: WebsocketBlindTestMessage) {
  // Handle the song new message
}

export function useGameWebsocket() {
  const ws = useWebSocket('ws://127.0.0.1:8000/ws/songs', {
    immediate: false,
    onConnected,
    onDisconnected,
    onError,
    onMessage(_ws, event: MessageEvent<string>) {
      const { parse } = useWebsocketMessage()
      const data = parse<WebsocketBlindTestMessage>(event.data)

      if (data) {
        switch (data.action) {
          case 'connection_token':
            handleConnectionToken(data)
            break

          case 'game_started':
            handleGameStarted(data)
            break

          case 'song_new':
            handleSongNew(data)
            break

          case 'timer_tick':
            break

          case 'guess_correct':
            break

          case 'song_skipped':
            break

          case 'randomize_genre':
            break

          case 'device_connected':
            break

          case 'device_disconnected':
            break

          case 'error':
            break

          default:
            break
        }
      }
    }
  })

  return {
    ws
  }
}
