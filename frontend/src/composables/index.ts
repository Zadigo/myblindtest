/* eslint-disable  @typescript-eslint/no-explicit-any */

export * from './use'

export function useCustomDebounce() {
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
};

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
