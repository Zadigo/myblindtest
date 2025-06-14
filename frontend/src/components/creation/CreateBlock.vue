<template>
  <div :data-id="index">
    <div class="flex justify-end mb-5">
      <VoltSecondaryButton rounded>
        <VueIcon icon="fa-solid:trash" />
      </VoltSecondaryButton>
    </div>

    <div class="grid grid-cols-3 gap-2">
      <VoltInputText v-model="requestData.name" placeholder="Song name" />
      <VoltAutocomplete v-model="requestData.genre" :suggestions="filteredGenres" :virtual-scroller-options="{ itemSize: 50 }" option-label="label" placeholder="Genre" dropdown @complete="searchGenres" />
      <VoltInputNumber v-model.number="requestData.year" placeholder="Year" />
    </div>

    <div class="w-9/12 my-2">
      <VoltInputNumber v-model="requestData.difficulty" :min="1" :max="5" placeholder="Difficulty" />
    </div>

    <div class="flex gap-2">
      <VoltInputText v-model="requestData.artist_name" placeholder="Artist" hint="Press shift+Enter to split and infer genre" @keypress.shift.enter="handleSplit" />
      <VoltInputText v-model="requestData.youtube_id" placeholder="YouTube" />
    </div>

    <div class="w-10/12">
      {{ requestData }}
      <VoltAutocomplete v-model="requestData.featured_artists" :suggestions="filteredArtists" :virtual-scroller-options="{ itemSize: 50 }" option-label="name" placeholder="Featured artists" multiple fluid dropdown @complete="searchArtists" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDayJs } from '@/plugins'
import { toast } from 'vue-sonner'

import type { Artist, CreateData, Song } from '@/types'

interface SearchEvent extends Event {
  query: string
}

const props = withDefaults(defineProps<{
  block?: CreateData
  index: number
}>(), {
  block() {
    return {
      name: '',
      genre: '',
      artist_name: '',
      featured_artists: [],
      youtube_id: '',
      year: 2025,
      difficulty: 1
    }
  }
})

const emit = defineEmits<{
  'update:block': [block: CreateData]
}>()

const { currentYear } = useDayJs()
const { client } = useAxiosClient()

const genres = inject<Ref<string[]>>('genres')

const searching = ref<boolean>(false)
const filteredArtists = ref<Artist[]>([])
const filteredGenres = ref<{ label: string, value: string }[]>([])

const featuredArtists = useStorage<Artist[]>('artists', [])

const fieldErrors = reactive({
  name: '',
  genre: '',
  artist: '',
  youtube: '',
  year: ''
})

// const iframe = ref<string>('')

const rules = {
  required: (v: string) => !!v || 'This field is required',
  youtubeUrl: (v: string) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/
    return youtubeRegex.test(v) || 'Please enter a valid YouTube URL'
  },
  difficulty: (v: number) => {
    return v <= 5 || 'Difficulty should be between 1 and 5'
  },
  year: (v: number | null) => {
    if (!v) {
      return true
    } else {
      return (v >= 1900 && v <= currentYear.value) || `Year must be between 1900 and ${currentYear.value}`
    }
  }
}

/**
 * Validation function
 */
function validateData(data: CreateData) {
  const errors: Record<string, string> = {}

  Object.keys(fieldErrors).forEach((key) => {
    fieldErrors[key as keyof typeof fieldErrors] = ''
  })

  if (!data.name) {
    errors.name = 'Name is required'
  }

  if (!data.genre) {
    errors.genre = 'Genre is required'
  }

  if (!data.artist_name) {
    errors.artist = 'Artist is required'
  }

  // Year validation (optional but must be valid if provided)
  if (!rules.year(data.year)) {
    errors.year = `Year must be between 1900 and ${currentYear}`
  }

  // Update field errors
  Object.entries(errors).forEach(([key, value]) => {
    fieldErrors[key as keyof typeof fieldErrors] = value
  })

  return errors
}

const requestData = computed({
  get: () => props.block,
  set: (value) => {
    const errors = validateData(value)
    console.log(errors)

    // Transform the block to only contain strings
    // of the artist's names
    const newBlock = { ...value }
    newBlock.featured_artists = value.featured_artists.map(x => x.name)

    emit('update:block', newBlock)
  }
})

const dictGenres = computed(() => {
  if (genres) {
    return genres.value.map(x => ({ label: x, value: x }))
  } else {
    return []
  }
})

/**
 * Allows the user to automatically infer the
 * current genre of the song based on a pre-existing
 * songs from the same artist from the database
 */
async function handleSearchExistingArtist() {
  try {
    searching.value = true
    const result = await client.get<Song[]>('/api/v1/songs/', {
      params: {
        q: requestData.value.artist_name
      }
    })

    const song = result.data[0]
    if (song) {
      requestData.value.genre = song.genre
    }

    searching.value = false
  } catch {
    toast.error('Could not perform search')
    searching.value = false
  }
}

/**
 *
 */
async function handleSplit() {
  if (requestData.value.artist_name.includes('-') && requestData.value.artist_name !== '') {
    const tokens = requestData.value.artist_name.split('-')
    requestData.value.artist_name = tokens[0].trim()
    requestData.value.name = tokens[1].trim()
    await handleSearchExistingArtist()
  }
}

/**
 *
 */
async function handleSearchFeaturedArtists() {
  try {
    if (featuredArtists.value.length === 0) {
      searching.value = true
      const response = await client.get<Artist[]>('/api/v1/songs/artists')
      featuredArtists.value = response.data
      searching.value = false
    }
  } catch {
    toast.error('Request failed')
    searching.value = false
  }
}

/**
 * Search genres in the database
 */
function searchGenres(e: SearchEvent) {
  filteredGenres.value = dictGenres.value.filter((x) => {
    const query = e.query
    return x.label.toLowerCase().includes(query.toLowerCase())
  })
}

/**
 * Search for existing artists in the database
 */
function searchArtists(e: SearchEvent) {
  filteredArtists.value = featuredArtists.value.filter((x) => {
    const query = e.query
    return x.name.toLowerCase().includes(query.toLowerCase())
  })
}

onBeforeMount(async () => {
  await handleSearchFeaturedArtists()
})
</script>
