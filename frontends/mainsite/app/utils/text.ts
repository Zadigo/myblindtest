import type { Arrayable } from '~/types'

/**
 * Adds string functionnalities like pluralization
 */
export function useString() {
  function plural(items: Arrayable<string | number | object>, word: string) {
    return (Array.isArray(items) ? items.length : items) > 1 ? `${word}s` : word
  }

  function generateRandomString(length: number) {
    const charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    const values = new Uint32Array(length)

    crypto.getRandomValues(values)
    return ref(Array.from(values, v => charset[ v % charset.length ]).join(''))
  }

  return {
    /**
     * Pluralizes a word based on the number of items
     * @param items The items to count
     * @param word The word to pluralize
     */
    plural,
    /**
     * Generates a random string of given length
     * @param length The length of the string to generate
     */
    generateRandomString
  }
}
