import type { Arrayable, GenreDistribution, SettingsApiResponse } from '~/types'

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
    return ref(Array.from(values, v => charset[v % charset.length]).join(''))
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


/**
 * Loads autocomplete data for the minimum and maximum time
 * period for the songs, the count by genre
 * 
 * @param fromCache Whether to load data from cache or fetch from API
 */
export const useLoadAutocompleteData = createSharedComposable((_fromCache = false) => {
  const autocomplete = ref<SettingsApiResponse | undefined>()

  // TODO: Memoize does not work properly
  const { load } = useMemoize(async (path: string) => {
    return await $fetch<SettingsApiResponse>(path, { baseURL: useRuntimeConfig().public.apiBaseUrl })
  })

  tryOnMounted(async () => { 
    autocomplete.value = await load('/api/v1/songs/settings')
  })

  const minimumPeriod = computed(() => autocomplete.value?.period.minimum || 0)
  const maximumPeriod = computed(() => autocomplete.value?.period.maximum || 100)
  const genreDistribution = computed<GenreDistribution[]>(() => autocomplete.value?.count_by_genre || [])
  const genres = useArrayMap(genreDistribution, (item) => ({ label: item.genre, name: item.genre }))
  const genreNames = useArrayMap(genreDistribution, (item) => item.genre)

  return {
    /**
     * Autocomplete data for the songs settings
     */
    autocomplete,
    /**
     * Minimum period for the songs
     * @default 0
     */
    minimumPeriod,
    /**
     * Maximum period for the songs
     * @default 100
     */
    maximumPeriod,
    /**
     * Distribution of genres for the songs
     * @default []
     */
    genreDistribution,
    /**
     * List of genres for the songs
     * @default []
     */
    genres,
    /**
     * List of genre names for the songs
     * @default []
     */
    genreNames
  }
})
