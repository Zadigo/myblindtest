import type { Ref } from 'vue'
import type { _ReceiveMessages, _SendMessages } from '@/types'

export * from './randomizer'
export * from './utils'
export * from './ws_manager'
export * from './ws_individual_manager'

/**
 * Composable used to handle websocket messages
 */
export function useWebsocketMessage<S = _SendMessages, R = _ReceiveMessages>() {
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
