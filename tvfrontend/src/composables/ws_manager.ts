import { toast } from 'vue-sonner'
import { useWebsocketMessage } from '.'
import type { WebsocketMessage, WebsocketReceiveMessage, WebsocketSendMessage } from '@/types'

/**
 *
 */
function handleOnConnected() {
  // Do something
}

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
function handleOnDisconnected() {
  // Do something
}


/**
 * @param ws Websocket
 * @param event The incoming event
 */
function handleOnMessage(isVerified: Ref<boolean>) {
  return (ws: WebSocket, event: MessageEvent<WebsocketReceiveMessage>) => {
    switch (event.data.action) {      
      case 'game_disconnected':
        // Handle game_disconnected action
        break
  
      case 'game_updates':
        // Handle game_updates action
        break
  
      case 'idle_connect':
        // Handle idle_connect action
        console.log(event)
        break
  
      case 'check_code':
        // Handle check_code action
        isVerified.value = event.data.valid
  
        if (isVerified.value) {
          toast.success('Pin code is valid', {
            position: 'top-center'
          })
        } else {
          toast.error('Pin code is invalid', {
            position: 'top-center'
          })
        }
        break
  
      default:
        break
    }
  }
}

/**
 * Composable for managing game websocket
 */
export function useGameWebsocket() {
  const { send } = useWebsocketMessage()
  const showAnswer = refAutoReset(false, 5000)
  
  const isVerified = ref<boolean>(false)

  const ws = useWebSocket('ws://127.0.0.1:8000/ws/connect', {
    immediate: false,
    onConnected: handleOnConnected,
    onError: handleOnError,
    onDisconnected: handleOnDisconnected,
    onMessage: handleOnMessage(isVerified)
  })

  const isConnected = computed(() => ws.status.value === 'OPEN')

  function connect() {
    ws.open()
    ws.send(send<Partial<WebsocketMessage>>({ action: 'idle_connect' }))
  }

  function checkPinCode(code: number) {
    ws.send(send<Partial<WebsocketSendMessage>>({ action: 'check_code', pinCode: code }))
  }
  
  return {
    /**
     * Connect to the websocket
     */
    connect,
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
    wsObject: ws,
    /**
     * The OTP code was returend correct
     */
    isVerified
  }
}
