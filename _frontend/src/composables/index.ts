export * from './use'

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
