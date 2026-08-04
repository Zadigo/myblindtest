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
