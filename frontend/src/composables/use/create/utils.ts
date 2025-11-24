/**
 * Returns the list of genres from the API
 */
export function useAutocompleteGenres<T = SearchedGenreApiResponse>() {
  const genres = useStorage<T[]>('genres', [])

  // TODO: Memoize does not work properly
  const { load, cache } = useMemoize(async (_key: number) => {
    const { execute, responseData } = useRequest<T[]>('django', '/api/v1/songs/genres')
    await execute()
    return responseData.value || []
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
