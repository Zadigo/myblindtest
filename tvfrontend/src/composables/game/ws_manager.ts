import type { WebsocketReceiveMessage } from '@/types'
import { toast } from 'vue-sonner'
import { useWebsocketMessage } from '.'

/**
 *
 */
function handleOnError() {
  toast('Failed to connect to websocket', {
    position: 'top-center'
  })
}

/**
 *
 */
function onDisconnected() {
  // Do something
}


/**
 * @param ws Websocket
 * @param event The incoming event
 */
function onMessage(ws: WebSocket, event: MessageEvent<WebsocketReceiveMessage>) {
  const connectionStore = useConnectionStore()
  
  console.log(ws)

  switch (event.data.action) { 
    case 'idle_connect':
      console.log('Connected')
      toast.info('Device ID', { description: event.data.message })
      break

    case 'device_accepted':
      toast.info('Device accepted')
      connectionStore.toggleIsAccepted()
      break
      
      case 'game_disconnected':
      connectionStore.toggleIsConnected()
      break

    case 'game_updates':
      // Handle game_updates action
      break

    default:
      break
  }
}

/**
 * Composable for managing game websocket
 */
export function useGameWebsocket() {
  const { stringify } = useWebsocketMessage()
  const showAnswer = refAutoReset(false, 5000)
  
  const ws = useWebSocket('ws://127.0.0.1:8000/ws/tv/connect', {
    immediate: false,
    onError: handleOnError,
    onDisconnected,
    onMessage
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
     * Show the answer to the blindtest
     */
    showAnswer,
    /**
     * Check if the websocket is connected
     */
    isConnected,
    /**
     * The websocket object
     */
    wsObject: ws
  }
}
