/**
 * Returns the list of genres from the API
 */
export function useAutocompleteGenres<T = SearchedGenreApiResponse>() {
  const genres = useLocalStorage<T[]>('genres', [])

  // TODO: Memoize does not work properly
  const { load } = useMemoize(async (_key: number) => {
    try {
      const responseData = await $fetch<T[]>('/api/v1/songs/genres', {
        method: 'GET',
        baseURL: useRuntimeConfig().public.apiBaseUrl
      })
      return responseData
    } catch (error) {
      console.error('Error fetching genres:', error)
      return []
    }
  })

  onMounted(async () => {
    genres.value = await load(1)
  })

  /**
   * Show songs
   */

  const [showSongs, toggleShowSongs] = useToggle<boolean>(false)

  return {
    /**
     * Toggle list display of songs
     * @default false
     */
    showSongs,
    /**
     * List of genres from the API
     */
    genres,
    /**
     * Toggle the display of songs
     */
    toggleShowSongs
  }
}
