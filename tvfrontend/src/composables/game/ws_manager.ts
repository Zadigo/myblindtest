import { toast } from 'vue-sonner'
import { useWebsocketMessage } from '.'

/**
 *
 */
function onError() {
  toast('Failed to connect to websocket', {
    position: 'top-center'
  })
  console.log('Failed to connect')
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
function onMessage(ws: WebSocket, event: MessageEvent<string>) {
  const connectionStore = useConnectionStore()
  const { showAnswer, answer } = storeToRefs(connectionStore)

  const { parse } = useWebsocketMessage()
  const parsedData = parse(event.data)
  
  console.log(ws, parsedData)

  if (parsedData) {
    switch (parsedData.action) {
      case 'idle_connect':
        console.log('Idle connect')
        toast.info('Device ID', { description: parsedData.message })
        connectionStore.toggleIsConnected()
        break
        
      case 'device_accepted':
        toast.info('Device accepted')
        connectionStore.toggleIsAccepted()
        console.log('Device accepted', connectionStore)
        break
        
      case 'game_disconnected':
        connectionStore.toggleIsConnected()
        break

      case 'guess_correct':
        showAnswer.value = true
        
        if (parsedData.song) {
          answer.value = parsedData.song
        }
        break

      case 'song_skipped':
        showAnswer.value = true

        if (parsedData.song) {
          answer.value = parsedData.song
        }
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
export function useGameWebsocket() {
  const { stringify } = useWebsocketMessage()

  const ws = useWebSocket('ws://127.0.0.1:8000/ws/tv/connect', {
    immediate: false,
    onError,
    onDisconnected,
    onMessage: onMessage
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
     */
    isConnected,
    /**
     * The websocket object
     */
    wsObject: ws
  }
}
