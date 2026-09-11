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
 * Loads autocomplete data for the minimum and maximum time
 * period for the songs, the count by genre
 * 
 * @param fromCache Whether to load data from cache or fetch from API
 */
export const useLoadAutocompleteData = createSharedComposable((_fromCache = false) => {
  const { data: autocomplete } = useAsyncData('autocomplete', () => $fetch<SettingsApiResponse>('/api/songs/settings', {
    method: 'GET'
  }), {
    default: () => ({ period: { minimum: 0, maximum: 100 }, count_by_genre: [] } as SettingsApiResponse)
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
