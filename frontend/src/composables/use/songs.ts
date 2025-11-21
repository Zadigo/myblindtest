import type { NewSong, Song } from '@/types'
import { useToast } from 'primevue/usetoast'

interface SongCreationApiResponse {
  errors: string[]
  items: Song[]
}

export interface SearchedGenreApiResponse {
  category: string
  items: { label: string }[]
}

/**
 * Returns the list of genres from the API
 */
export function useGetGenres<T = SearchedGenreApiResponse>() {
  /**
   * Genres
   */
  const genres = useStorage<T[]>('genres', [])

  const { load, cache } = useMemoize(async (_key: number) => {
    const { execute, responseData } = useRequest<T[]>('django', '/api/v1/songs/genres')
    await execute()
    return responseData.value || []
  })

  onMounted(async () => {
    genres.value = await load(1)
  })

  console.log('Genres cache:', cache)

  // const { execute, responseData } = useRequest<T[]>('django', '/api/v1/songs/genres')

  // onMounted(async () => {
  //   await execute()
  //   genres.value = responseData.value || []
  // })

  /**
   * Show songs
   */

  const [showSongs, toggleShowSongs] = useToggle<boolean>(false)

  return {
    showSongs,
    genres,
    toggleShowSongs
  }
}

/**
 * Composable for editing a song
 */
export const useEditSong = createSharedComposable(() => {
  const toast = useToast()
  
  const blocks = ref<NewSong[]>([
    {
      name: '',
      genre: '',
      artist_name: '',
      featured_artists: [],
      youtube_id: '',
      year: 0,
      difficulty: 1
    }
  ])

  const cleanedData = computed(() => {
    return blocks.value.map((block) => ({
      ...block,
      // featured_artists: block.featured_artists.join(','),
      genre: typeof block.genre === 'string' ? block.genre : block.genre.label,
      artist_name: typeof block.artist_name === 'string' ? block.artist_name : block.artist_name.label
    })) as NewSong[]
  })

  async function _save() {
    const { responseData } = await useAsyncRequest<SongCreationApiResponse>('django', '/api/v1/songs/create', {
      method: 'post',
      body: cleanedData.value,
      immediate: true
    })

    if (responseData.value) {
      if (responseData.value.errors.length > 0) {
        toast.add({
          severity: 'error', 
          summary: 'Error when creating songs', 
          detail: responseData.value.errors.join(', '), 
          life: 10000
        })
      }
    }
  }

  const save = useThrottleFn(async () => { await _save() }, 5000)

  function addBlock() {
    blocks.value.push({
      name: '',
      genre: '',
      artist_name: '',
      featured_artists: [],
      youtube_id: '',
      year: 0,
      difficulty: 1
    })
  }

  function deleteBlock(index: number) {
    blocks.value.splice(index, 1)
  }

  /**
   * Block
   */

  const getCurrentBlock = reactify((index: number) => blocks.value[index])

  return {
    /**
     * Songs to create
     */
    blocks,
    /**
     * Cleaned data to send to the API
     * @private
     */
    cleanedData,
    /**
     * Save the songs
     */
    save,
    /**
     * Add a new block to the songs
     */
    addBlock,
    /**
     * Delete a block from the songs
     */
    deleteBlock,
    /**
     * Get the current block by index to edit
     * @param index Index of the block
     */
    getCurrentBlock
  }
})
