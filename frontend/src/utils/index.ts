export function generateRandomString(length: number) {
  const charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
  const values = new Uint32Array(length)
  crypto.getRandomValues(values)
  return ref(Array.from(values, v => charset[v % charset.length]).join(''))
}

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
