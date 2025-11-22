import type { CacheSession, IndividualBlindTestPlayer } from '@/types'
import { doc, updateDoc } from 'firebase/firestore'
import { useToast } from 'primevue/usetoast'
import { useDocument, useFirestore } from 'vuefire'


export type SendIndividualBlindTestMessage = { action: 'test' }

export type ReceiveIndividualBlindTestMessage = { action: 'device_accepted', players: Record<string, IndividualBlindTestPlayer> }
  | { action: 'device_disconnected', players: Record<string, IndividualBlindTestPlayer> }
  | { action: 'idle_connect', session_id: string, player: IndividualBlindTestPlayer }


/**
 * Websocket for individual game (admin)
 */
export const useGameWebsocketIndividual = createSharedComposable(() => {
  const { sessionId } = useSession()

  /**
   * Message
   */

  const { parse } = useWebsocketMessage<SendIndividualBlindTestMessage, ReceiveIndividualBlindTestMessage>()

  /**
   * Websocket
   */
  const toast = useToast()
  const fireStore = useFirestore()
  const docRef = doc(fireStore, 'blindtests', sessionId.value)
  const gameStarted = ref(false)

  const wsObject = useWebSocket(`ws://127.0.0.1:8000/ws/songs/${sessionId.value}/single-player`, {
    immediate: false,
    onMessage: async (_ws, event: MessageEvent) => {
      const message = parse(event.data)

      if (isDefined(message)) {
        if (message.action === 'device_accepted') {
          await updateDoc(docRef, { players: message.players })
          toast.add({ severity: 'info', summary: 'Device connected', detail: `Player has connected.`, life: 3000 })
        }

        if (message.action === 'device_disconnected') {
          await updateDoc(docRef, { players: message.players })
          toast.add({ severity: 'warn', summary: 'Device disconnected', detail: `Player has disconnected.`, life: 3000 })
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

  /**
   * Actions
   */

  function startGame() {}

  function stopGame() {}

  return {
    gameStarted,
    wsObject,
    isConnected,
    blindTestDoc,
    players,
    startGame,
    stopGame
  }
})

/**
 * Websocket for individual player (smartphone)
 */
export const useGameWebsocketIndividualPlayer = createSharedComposable(() => {
  const route = useRoute()

  /**
   * Websocket
   */
  const toast = useToast()
  const fireStore = useFirestore()
  const { parse } = useWebsocketMessage<SendIndividualBlindTestMessage, ReceiveIndividualBlindTestMessage>()

  const playerId = useLocalStorage<string>('playerId', '')

  const wsObject = useWebSocket(`ws://127.0.0.1:8000/ws/single-player/${route.params.id}/connect`, {
    immediate: false,
    onConnected: async (_ws) => {
      toast.add({ severity: 'info', summary: 'Connected', detail: 'WebSocket connected for individual player', life: 3000 })
    },
    onDisconnected: (_ws, _event) => {
      toast.add({ severity: 'warn', summary: 'Disconnected', detail: 'WebSocket disconnected for individual player', life: 3000 })
    },
    onMessage: async (_ws, event: MessageEvent) => {
      const message = parse(event.data)

      if (message?.action === 'idle_connect') {
        playerId.value = message.player.name
      }
    }
  })

  /**
   * State
   */

  const isConnected = computed(() => wsObject.status.value === 'OPEN')

  const docRef = doc(fireStore, 'blindtests', route.params.id as string)
  const blindTestDoc = useDocument<CacheSession>(docRef)
  const player = computed(() => blindTestDoc.value?.players[playerId.value])

  return {
    wsObject,
    isConnected,
    blindTestDoc,
    player
  }
})
