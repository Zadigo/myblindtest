import type { Arrayable } from '@/types'

/**
 * Adds string functionnalities like pluralization
 */
export function useString() {
  function plural(items: Arrayable<string | number | object>, word: string) {
    return (Array.isArray(items) ? items.length : items) > 1 ? `${word}s` : word
  }

  return {
    /**
     * Pluralizes a word based on the number of items
     * @param items The items to count
     * @param word The word to pluralize
     */
    plural
  }
}

/**
 * Global state used to share UI state across components in the application
 * such as modals visibility and other global flags
 */
export const useGlobalState = createGlobalState(() => {
  const [showAbout, toggleShowAbout] = useToggle(false)
  const [showConnectionUrl, toggleShowConnectionUrl] = useToggle(false)

  return {
    /**
     * Whether to show the About modal
     * @default false
     */
    showAbout,
    /**
     * Whether to show the Connection URL modal
     * @default false
     */
    showConnectionUrl,
    /**
     * Toggles the About modal visibility
     */
    toggleShowAbout,
    /**
     * Toggles the Connection URL modal visibility
     */
    toggleShowConnectionUrl
  }
})

/**
 * Composable to manage dark mode state
 */
export const useDarkMode = createSharedComposable(() => {
  const isDark = useDark({ selector: 'html', attribute: 'class', valueDark: 'p-dark', })
  const toggleDark = useToggle(isDark)

  return {
    /**
     * Whether dark mode is enabled
     * @default false
     */
    isDark,
    /**
     * Toggles dark mode
     */
    toggleDark
  }
})
