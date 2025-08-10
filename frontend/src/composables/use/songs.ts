import { toast } from 'vue-sonner'
import { addNewSongData } from '@/data'

import type { NewSong, Song } from '@/types'

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

export function useEditSong() {
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

  // const featuredArtists = useStorage<Artist[]>('artists', [])

  async function save() {
    // const transformedRequestData: CopiedCreateData[] = blocks.value.map((item) => {
    //   if (item.featured_artists.length > 0) {
    //     const copiedItem = { ...item }
    //     const featuredArists = copiedItem.featured_artists.join(',')

    //     copiedItem.featured_artists = featuredArists

    //     return copiedItem
    //   } else {
    //     return item
    //   }
    // })

    const { responseData } = await useAsyncRequest<SongCreationApiResponse>('django', '/api/v1/songs/create', {
      method: 'post',
      body: blocks.value,
      immediate: true
    })

    if (responseData.value) {
      if (responseData.value.errors.length > 0) {
        toast.error(`Error when creating songs: ${responseData.value.errors}`, { duration: 10000 })
      }
    }

    blocks.value = [{ ...addNewSongData }]
  }

  function addBlock() {
    blocks.value.push({ ...addNewSongData })
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
