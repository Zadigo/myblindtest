import type { GenreDistribution, SettingsDataApiResponse } from '@/types'

export * from './songs'

/**
 * Loads autocomplete data for the minimum and maximum time
 * period for the songs, the count by genre
 */
export function useLoadAutocompleteData(fromCache = false) {
  const autocomplete = useStorage<SettingsDataApiResponse>('autocomplete', null)

  onBeforeMount(async () => {
    if (!fromCache) {
      const { responseData } = await useAsyncRequest<SettingsDataApiResponse>('django', '/api/v1/songs/settings', { method: 'get', immediate: true })
      syncRef(autocomplete, responseData, { direction: 'ltr' })
    }
  })

  const minimumPeriod = computed(() => autocomplete.value?.period.minimum || 0)
  const maximumPeriod = computed(() => autocomplete.value?.period.maximum || 100)
  const genreDistribution = computed<GenreDistribution[]>(() => autocomplete.value?.count_by_genre || [])

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
    genreDistribution
  }
}
