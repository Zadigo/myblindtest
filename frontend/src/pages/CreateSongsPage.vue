<template>
  <section class="my-5 px-10">
    <Suspense v-if="showSongs">
      <template #default>
        <AsyncListSongs @back="showSongs=false" />
      </template>

      <template #fallback>
        <section id="list">
          <div class="mx-auto w-6/12">
            <VoltSkeleton class="w-[200px] h-[200px]" />
          </div>
        </section>
      </template>
    </Suspense>

    <div v-else class="w-6/12 mx-auto">
      <VoltCard class="border-none">
        <template #content>
          <TransitionGroup name="opacity">
            <template v-for="(block, i) in blocks" :key="i">
              <CreateBlock :block="block" :index="i" />
              <VoltDivider v-if="blocks.length > 1 && i !== blocks.length - 1" class="my-5" />
            </template>
          </TransitionGroup>
        </template>

        <template #footer>
          <div class="space-x-2">
            <VoltButton class="ms-auto" @click="handleAddBlock">
              <VueIcon icon="fa-solid:plus" />Add block
            </VoltButton>

            <VoltButton @click="handleSave">
              <VueIcon icon="fa-solid:save" />
              Save
            </VoltButton>

            <VoltButton @click="showSongs=true">
              <VueIcon icon="fa-solid:table" />
              Songs
            </VoltButton>
          </div>
        </template>
      </VoltCard>
    </div>
  </section>
</template>

<script setup lang="ts">
import { addNewSongData } from '@/data'
import { Artist, CopiedCreateData, CreateData, Song } from '@/types'
import { toast } from 'vue-sonner'

interface SongCreationApiResponse {
  errors: string[]
  items: Song[]
}

// useHead({
//   title: ' Create new song',
//   meta: [
//     {
//       name: 'description',
//       content: 'Write a description here'
//     }
//   ]
// })

const AsyncListSongs = defineAsyncComponent({
  loader: async () => import('@/components/creation/ListSongs.vue'),
  timeout: 20000
})

const { client } = useAxiosClient()

/**
 * c: Create
 * l: List of songs
 */
const searchParam = useUrlSearchParams('history', {
  initialValue: {
    v: 'c'
  } as {
    v: 'l' | 'c'
  }
})

const showSongs = ref<boolean>(false)
const blocks = ref<CreateData[]>([
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

const genres = useStorage<string[]>('genres', [])
const featuredArtists = useStorage<Artist[]>('artists', [])

/**
 * Search within the list of available artists
 */
async function handleSearchFeaturedArtists() {
  try {
    const response = await client.get<Artist[]>('/songs/artists')
    featuredArtists.value = response.data
  } catch (e) {
    toast.error(`Request failed: ${e}`)
  }
}

/**
 * Save the new song to the database
 */
async function handleSave() {
  try {
    // Transform the list so that the featured artists
    // is a comma separated string
    const transformedRequestData: CopiedCreateData = blocks.value.map((item) => {
      if (item.featured_artists.length > 0) {
        const copiedItem = { ...item }
        const featuredArists = copiedItem.featured_artists.join(',')
        copiedItem.featured_artists = featuredArists
        return copiedItem
      } else {
        return item
      }
    })

    const response = await client.post<SongCreationApiResponse>('/api/v1/songs/create', transformedRequestData)
    blocks.value = [{ ...addNewSongData }]

    if (response.data.errors.length > 0) {
      toast.error(`Error when creating songs: ${response.data.errors}`, {
        duration: 10000
      })
    } else {
      await handleSearchFeaturedArtists()
    }
  } catch {
    toast.error('Could not create songs')
  }
}

/**
 * Get all the available genres from
 * the backend
 */
async function handleGetGenres() {
  try {
    if (genres.value.length === 0) {
      const response = await client.get<string[]>('/api/v1/songs/genres')
      genres.value = response.data
    }
  } catch {
    toast.error('Failed to get genres')
  }
}

function handleAddBlock() {
  blocks.value.push({ ...addNewSongData })
}

provide('genres', genres)

onMounted(async () => {
  await handleGetGenres()

  if (searchParam.v === 'l') {
    showSongs.value = true
  }
})
</script>
