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
 * Global state used to share UI state across components in the application
 * such as modals visibility and other global flags
 */
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
