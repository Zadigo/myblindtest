/**
 * Returns the list of genres from the API
 */
export function useAutocompleteGenres<T = SearchedGenreApiResponse>() {
  const { data: genres } = useAsyncData('genres', () => $fetch<T[]>('/api/songs/genres', {
    method: 'GET'
  }), {
    default: () => [] as T[]
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
