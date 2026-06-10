import { useToast } from 'primevue/usetoast'
import type { PrimeVueToast } from '@/types'
import { useWebsocketMessage } from '.'

function onError(toast: PrimeVueToast) {
  toast.add({ detail: 'An error occurred with the websocket connection', severity: 'error', summary: 'Websocket error' })
}

function onDisconnected(toast: PrimeVueToast) {
  toast.add({ detail: 'Websocket connection lost', severity: 'error', summary: 'Websocket disconnected' })
}

/**
 * @param ws Websocket
 * @param event The incoming event
 */
function onMessage(ws: WebSocket, event: MessageEvent<string>, toast: PrimeVueToast, store: ReturnType<typeof useGameStore>) {
  const { parse } = useWebsocketMessage()
  const parsedData = parse(event.data)
  
  console.log(ws, parsedData)

  if (parsedData) {
    switch (parsedData.action) {
      case 'idle_connect':
        console.log('Idle connect')
        toast.add({ detail: 'Connected to server', severity: 'info', summary: 'Websocket connected' })
        break
        
      case 'device_accepted':
        toast.add({ detail: 'Device accepted', severity: 'info', summary: 'Device accepted' })
        break
        
      case 'game_disconnected':
        toast.add({ detail: 'Game disconnected', severity: 'warn', summary: 'Game disconnected' })
        break

      case 'guess_correct':
        if (parsedData.song) {
          store.showAnswer = true
          store.answer = parsedData.song
          store.correctAnswerTeamId = parsedData.team_id
        }
        break

      case 'song_skipped':
        store.showAnswer = true
        console.log(parsedData)
        if (parsedData.song) store.answer = parsedData.song
        break
  
      case 'game_updates':
        break
  
      default:
        console.log('No action provided', parsedData)
        break
    }
  } else {
    console.error('No data was provided')
  }
}

/**
 * Composable for managing game websocket
 */
export const useGameWebsocket = createGlobalState(() => {
  const toast = useToast()
  const { stringify } = useWebsocketMessage()
  const isAccepted = ref<boolean>(false)

  const gameStore = useGameStore()

  const ws = useWebSocket('ws://127.0.0.1:8000/ws/tv/connect', {
    immediate: false,
    onError: () => onError(toast),
    onDisconnected: () => onDisconnected(toast),
    onMessage: (ws, event) => onMessage(ws, event, toast, gameStore)
  })

  const isConnected = computed(() => ws.status.value === 'OPEN')

  function connect() {
    ws.open()
    ws.send(stringify({ action: 'idle_connect' }))
  }

  function checkPinCode(code: string) {
    ws.send(stringify({ action: 'check_code', pinCode: code }))
  }
  
  return {
    /**
     * Connect to the websocket
     */
    connect,
    /**
     * Function used to check the pin code and
     * determine whether the device is accepted
     * within the list of accepted devices
     */
    checkPinCode,
    /**
     * Check if the websocket is connected
     * @default false
     */
    isConnected,
    /**
     * Whether the connection token is accepted
     * for the given blindtest
     * @default false
     */
    isAccepted,
    /**
     * The websocket object
     */
    ws
  }
})
