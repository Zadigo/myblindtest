import type { RandomizerData } from '@/components/randomizer'
import type { WebsocketReceiveMessage, WebsocketSendMessage } from '@/types'
import type { Ref } from 'vue'

export * from './ws_manager'

/**
 * Composable used to handle websocket messages
 */
export function useWebsocketMessage<S = Partial<WebsocketSendMessage>, R = Partial<WebsocketReceiveMessage>>() {
  function parse(data: string): R | undefined {
    try {
      return JSON.parse(data) as R
    } catch (e) {
      console.error("Failed to parse websocket message", e)
      return undefined
    }
  }

  function stringify(data: S): string {
    return JSON.stringify(data)
  }

  function parseToRef(data: string): Ref<R | undefined> {
    return toRef(parse(data)) as Ref<R | undefined>
  }

  return {
    /**
     * Parses the given data received from the websocket
     */
    parse,
    /**
     * Parses the given data received from the websocket and returns a ref
     */
    parseToRef,
    /**
     * Stringifies the given data for sending over the websocket
     */
    stringify
  }
}

/**
 * Composable that triggers and runs the
 * wheel randomizer
 */
export function useWheelRandomizer(ws: Ref<WebSocket | undefined>) {
  const showWheel = ref<boolean>(false)
  const randomizerEl = ref<HTMLElement>()

  const { stringify } = useWebsocketMessage()

  /**
   * Function that gets called once the
   * spinning has finished
   *
   * @param value The genre to get
   */
  function randomizerComplete(value: string | undefined | RandomizerData) {
    if (value) {
      setTimeout(() => {
        showWheel.value = false

        const result = stringify({
          action: 'randomize_genre',
          temporary_genre: value
        })

        if (result && ws.value) {
          ws.value.send(result)
        }
      }, 3000)
    }
  }

  return {
    showWheel,
    randomizerEl,
    randomizerComplete
  }
}
