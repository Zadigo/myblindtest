import type { GenreDistribution, SettingsApiResponse } from '@/types'

export * from './create'
export * from './game'
export * from './session'
export * from './songs'

/**
 * Loads autocomplete data for the minimum and maximum time
 * period for the songs, the count by genre
 * 
 * @param fromCache Whether to load data from cache or fetch from API
 */
export const useLoadAutocompleteData = createSharedComposable((fromCache = false) => {
  const autocomplete = useLocalStorage<SettingsApiResponse>('autocomplete', null, {
    serializer: {
      write: (value) => JSON.stringify(value),
      read: (value) => (value ? JSON.parse(value) : null)
    }
  })

  onBeforeMount(async () => {
    if (!fromCache) {
      const { responseData } = await useAsyncRequest<SettingsApiResponse>('django', '/api/v1/songs/settings', { method: 'get', immediate: true })
      syncRef(autocomplete, responseData, { direction: 'rtl' })
    }
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
     */
    minimumPeriod,
    /**
     * Maximum period for the songs
     */
    maximumPeriod,
    /**
     * Distribution of genres for the songs
     */
    genreDistribution,
    /**
     * List of genres for the songs
     */
    genres,
    /**
     * List of genre names for the songs
     */
    genreNames
  }
})
