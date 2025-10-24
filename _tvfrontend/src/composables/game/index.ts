import type { WebsocketReceiveMessage, WebsocketSendMessage } from '@/types'

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
