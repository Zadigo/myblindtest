<template>
  <section class="my-5">
    <Suspense v-if="showSongs">
      <template #default>
        <AsyncListSongs @back="showSongs=false" />
      </template>

      <template #fallback>
        <span class="loader-5" />
      </template>
    </Suspense>

    <div v-else class="col-sm-12 col-md-6 offset-md-3">
      <div class="card shadow-sm">
        <TransitionGroup name="opacity">
          <template v-for="(block, i) in blocks" :key="i">
            <CreateBlock :block="block" :index="i" />
            <hr v-if="blocks.length > 1 && i !== blocks.length - 1" class="my-5">
          </template>
        </TransitionGroup>

        <div class="card-body d-flex gap-2">
          <v-btn variant="tonal" color="dark" @click="handleAddBlock">
            <FontAwesomeIcon class="me-2" icon="plus" />Add block
          </v-btn>

          <v-btn variant="tonal" color="dark" @click="handleSave">
            Save
          </v-btn>

          <v-btn variant="tonal" color="dark" @click="showSongs=true">
            Songs
          </v-btn>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { addNewSongData } from '@/data'
import { useAxiosClient } from '@/plugins/client'
import { Artist, CopiedCreateData, CreateData, Song } from '@/types'
import { useLocalStorage } from '@vueuse/core'
import { useHead } from 'unhead'
import { toast } from 'vue-sonner'

interface SongCreationApiResponse {
  errors: string[]
  items: Song[]
}

useHead({
  title: ' Create new song',
  meta: [
    {
      name: 'description',
      content: 'Write a description here'
    }
  ]
})

const AsyncListSongs = defineAsyncComponent({
  loader: async () => import('@/components/creation/ListSongs.vue'),
  timeout: 20000
})

const { client } = useAxiosClient()

const showSongs = ref(false)
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

const genres = useLocalStorage<string[]>('genres', [], {
  serializer: {
    read(raw) {
      return JSON.parse(raw)
    },
    write(value) {
      return JSON.stringify(value)
    }
  }
})

const featuredArtists = useLocalStorage<Artist[]>('artists', null, {
  serializer: {
    read(raw) {
      return JSON.parse(raw)
    },
    write(value) {
      return JSON.stringify(value)
    }
  }
})

async function handleSearchFeaturedArtists() {
  try {
    const response = await client.get<Artist[]>('/songs/artists')
    featuredArtists.value = response.data
  } catch (e) {
    toast.error('Request failed')
  }
}

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

    const response = await client.post<SongCreationApiResponse>('/songs/create', transformedRequestData)
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

// Get all the available genres from
// the backend
async function handleGetGenres() {
  try {
    if (genres.value) {
      if (genres.value.length === 0) {
        const response = await client.get<string[]>('/songs/genres')
        genres.value = response.data
      }
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
})
</script>
