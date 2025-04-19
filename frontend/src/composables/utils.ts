/* eslint-disable  @typescript-eslint/no-explicit-any */

import { ref } from 'vue'

export function useDebounce() {
  function debounce<T extends (...args: any[]) => void>(func: T, wait: number, immediate: boolean = false) {
    let timeout: ReturnType<typeof setTimeout> | null = null

    // return function (this: any, ...callbackArgs: Parameters<T>) {
    return function (...callbackArgs: Parameters<T>) {
      // const context = this

      function later() {
        timeout = null

        if (!immediate) {
          // func.apply(context, callbackArgs)
          func.apply(callbackArgs)
        }
      }

      const callNow = immediate && !timeout

      if (timeout) {
        clearTimeout(timeout)
      }
      timeout = setTimeout(later, wait)

      if (callNow) {
        // func.apply(context, callbackArgs)
        func.apply(callbackArgs)
      }
    }
  }

  return {
    debounce
  }
}

export function useLimitOffeset() {
  const paginationUrl = ref<URL>()

  function parser(url: string | null | undefined, limit = 100, offset = 100) {
    let defaultLimit: string | number = 100
    let defaultOffset: string | number = 0

    if (url) {
      paginationUrl.value = new URL(url)

      const potentialLimit = paginationUrl.value.searchParams.get('limit')
      const potentialOffset = paginationUrl.value.searchParams.get('offset')

      defaultLimit = potentialLimit || limit
      defaultOffset = potentialOffset || offset
    }

    const query = new URLSearchParams({ limit: defaultLimit.toString(), offset: defaultOffset.toString() }).toString()

    return {
      query,
      limit: defaultLimit,
      offset: defaultOffset
    }
  }

  return {
    parser
  }
}

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

export function useWebsocketUtilities() {
  function sendMessage<T>(data: T) {
    return JSON.stringify(data)
  }

  function parseMessage<T>(data: string): T {
    return JSON.parse(data)
  }

  return {
    sendMessage,
    parseMessage
  }
}
