<template>
  <CardContent :data-id="index">
    <div class="flex gap-2">
      <Input v-model="requestData.name" :rules="[rules.required]" type="text" placeholder="Name" variant="solo-filled" clearable flat />
      <v-combobox v-model="requestData.genre" :items="genres" :loading="searching" :rules="[rules.required]" type="text" variant="solo-filled" flat />
      <Input v-model.number="requestData.year" :rules="[rules.year]" type=" text" placeholder="Year" variant="solo-filled" flat />
    </div>

    <div class="w-4/12 my-2">
      <Input v-model="requestData.difficulty" :rules="[rules.difficulty]" :min="1" :max="5" type="number" placeholder="Difficulty" variant="solo-filled" flat />
    </div>

    <div class="flex gap-2">
      <Input v-model="requestData.artist_name" :rules="[rules.required]" type="text" placeholder="Artist" hint="Press shift+Enter to split and infer genre" variant="solo-filled" clearable flat @keypress.shift.enter="handleSplit" />
      <Input v-model="requestData.youtube_id" :rules="[rules.required]" type="text" placeholder="YouTube" variant="solo-filled" clearable flat />
    </div>

    <div class="w-10/12">
      <v-combobox v-model="requestData.featured_artists" :items="featuredArtists" :return-object="false" item-title="name" item-value="name" variant="solo-filled" placeholder="Featured artists" clearable flat chips multiple />
    </div>
  </CardContent>
</template>

<script setup lang="ts">
import { useDayJs } from '@/plugins'
import { toast } from 'vue-sonner'

import type { Artist, CreateData, Song } from '@/types'

const { currentYear } = useDayJs()

const props = defineProps({
  block: {
    type: Object as PropType<CreateData>,
    default: () => ({
      name: '',
      genre: '',
      artist_name: '',
      featured_artists: [],
      youtube_id: '',
      year: null,
      difficulty: 1
    })
  },
  index: {
    type: Number,
    required: true
  }
})

const emit = defineEmits({
  'update:block'(_data: CreateData) {
    return true
  }
})

const { client } = useAxiosClient()

const searching = ref<boolean>(false)
const genres = inject<string[]>('genres')

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

  // YouTube URL validation
  // if (!data.youtube) {
  //   errors.youtube = 'YouTube video ID is required';
  // } else if (!rules.youtubeUrl(data.youtube_id)) {
  //   errors.youtube = 'Please enter a valid YouTube URL';
  // }

  // Year validation (optional but must be valid if provided)
  if (data.year !== null && !rules.year(data.year)) {
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
    emit('update:block', value)
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
    const result = await client.get<Song[]>('/songs/', {
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
      const response = await client.get<Artist[]>('/songs/artists')
      featuredArtists.value = response.data
      searching.value = false
    }
  } catch {
    toast.error('Request failed')
    searching.value = false
  }
}

onBeforeMount(async () => {
  await handleSearchFeaturedArtists()
})
</script>
