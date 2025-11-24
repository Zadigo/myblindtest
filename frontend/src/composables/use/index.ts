import { useAsyncRequest } from 'vue-axios-manager'
import type { GenreDistribution, SettingsApiResponse } from '@/types'

export * from './create'
export * from './game'
export * from './session'
export * from './utils'

/**
 * Loads autocomplete data for the minimum and maximum time
 * period for the songs, the count by genre
 * 
 * @param fromCache Whether to load data from cache or fetch from API
 */
export const useLoadAutocompleteData = createSharedComposable((fromCache = false) => {
  const autocomplete = ref<SettingsApiResponse | undefined>()

  const { load } = useMemoize(async (path: string) => {
    const { responseData } = await useAsyncRequest<SettingsApiResponse>('django', path, { immediate: true })
    return responseData.value
  })

  onMounted(async () => { autocomplete.value = await load('/api/v1/songs/settings') })

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

/**
 * Composable to manage dark mode state
 */
export const useDarkMode = createSharedComposable(() => {
  const isDark = useDark({ selector: 'html', attribute: 'class', valueDark: 'p-dark',})
  const toggleDark = useToggle(isDark)

  return {
    isDark,
    toggleDark
  }
})
