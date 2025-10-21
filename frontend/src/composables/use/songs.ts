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
 * Returns the list of songs from the Api
 */
export function useGetGenres<T = SearchedGenreApiResponse>() {
  const genres = useStorage<T[]>('genres', [])
  const { execute, responseData } = useRequest<T[]>('django', '/api/v1/songs/genres')

  onMounted(async () => {
    await execute()
    genres.value = responseData.value || []
  })

  const showSongs = ref<boolean>(false)

  return {
    showSongs,
    genres
  }
}

/**
 * Composable for editing a song
 */
export function useEditSong() {
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

  async function save() {
    const { responseData } = await useAsyncRequest<SongCreationApiResponse>('django', '/api/v1/songs/create', {
      method: 'post',
      body: blocks.value.map((block) => ({
        name: block.name,
        genre: block.genre.label,
        artist_name: block.artist_name.label,
        featured_artists: block.featured_artists,
        youtube_id: block.youtube_id,
        year: block.year,
        difficulty: block.difficulty
      })),
      immediate: true
    })

    if (responseData.value) {
      if (responseData.value.errors.length > 0) {
        toast.add({ severity: 'error', summary: 'Error when creating songs', detail: responseData.value.errors.join(', '), life: 10000 })
      }
    }
  }

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

  return {
    /**
     * Songs to create
     */
    blocks,
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
    deleteBlock
  }
}
