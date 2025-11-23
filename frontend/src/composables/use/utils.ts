import type { WsSendMessage, WsReceiveMessage } from "./game"

export function useString() {
  function plural(items: (string | number | object)[], word: string) {
    if (items.length === 0 || items.length > 1) {
      return `${word}s`
    } else {
      return word
    }
  }

  return {
    plural
  }
}

/**
 * Composable used to handle websocket messages
 */
export function useWebsocketMessage<S = WsSendMessage, R = WsReceiveMessage>() {
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

export const useGlobalState = createGlobalState(() => {
  const [showAbout, toggleShowAbout] = useToggle(false)
  const [showConnectionUrl, toggleShowConnectionUrl] = useToggle(false)

  return {
    showAbout,
    toggleShowAbout,
    showConnectionUrl,
    toggleShowConnectionUrl
  }
})
