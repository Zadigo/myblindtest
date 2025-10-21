<template>
  <div :data-id="index">
    <div class="flex justify-end mb-5">
      <volt-secondary-button rounded @click="emit('delete:block', index)">
        <vue-icon icon="fa-solid:trash" />
      </volt-secondary-button>
    </div>

    <div class="grid grid-cols-3 gap-2">
      <volt-input-text v-model="newArtistSong.name" placeholder="Song name" />
      <volt-autocomplete v-model="newArtistSong.genre" :suggestions="filteredGenres" :virtual-scroller-options="{ itemSize: 50 }" option-label="label" option-group-children="items" option-group-label="category" placeholder="Genre" dropdown @complete="searchGenreComplete" />
      <volt-input-number v-model.number="newArtistSong.year" placeholder="Year" />
    </div>

    <div class="w-9/12 my-2">
      <volt-input-number v-model="newArtistSong.difficulty" :min="1" :max="5" placeholder="Difficulty" />
    </div>

    <div class="flex gap-2">
      <div class="flex-col">
        <volt-autocomplete v-model="newArtistSong.artist_name" :suggestions="artistSuggestions" :virtual-scroller-options="{ itemSize: 50 }" option-label="label" placeholder="Artist name" dropdown @complete="() => refresh({ q: newArtistSong.artist_name })" />
        <p class="text-xs italic">
          Appuyez sur Shif+Entrée pour split
        </p>
      </div>

      <volt-input-text v-model="newArtistSong.youtube_id" placeholder="YouTube" />
    </div>

    <div class="w-10/12">
      <!-- <volt-autocomplete v-model="newArtistSong.featured_artists" :suggestions="filteredArtists" :virtual-scroller-options="{ itemSize: 50 }" option-label="name" placeholder="Featured artists" multiple fluid dropdown @complete="searchArtists" /> -->
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { SearchedGenreApiResponse } from '@/composables'
import type { Artist, NewSong } from '@/types'

const defaultProps = withDefaults(defineProps<{ block?: NewSong, index?: number }>(), {
  block: () => ({
    name: '',
    genre: '',
    year: 2023,
    difficulty: 1,
    artist_name: '',
    featured_artists: [],
    youtube_id: ''
  }),
  index: 0
})

const emit = defineEmits<{ 'update:block': [block: NewSong], 'delete:block': [index: number] }>()

/**
 * Genres suggestions
 */

interface SearchEvent extends Event {
  query: string
}

const injectedGenres = inject<Ref<SearchedGenreApiResponse[]> | undefined>('genres')
const filteredGenres = ref<SearchedGenreApiResponse[]>([])

/**
 * Callback function for VoltAutocomplete component
 * to filter genres based on user input
 * @param event - The search event containing the query
 */
function searchGenreComplete(event: SearchEvent) {
  if (injectedGenres) {
    const items = injectedGenres.value.filter((genre) => {
      return genre.items.map(item => item.label.toLowerCase().includes(event.query.toLowerCase())).some(Boolean)
    })

    const filteredItems = []

    for (const genre of items) {
      const newGenre = {
        category: genre.category,
        items: genre.items.filter(item => item.label.toLowerCase().includes(event.query.toLowerCase()))
      }
      filteredItems.push(newGenre)
    }

    filteredGenres.value = filteredItems
  } else {
    return []
  }
}

/**
 * Artists suggestions
 */

const newArtistSong = computed({
  get: () => defaultProps.block,
  set: (value: NewSong) => {
    emit('update:block', value)
  }
})

const { responseData, execute: searchArtists, refresh } = useRequest<Artist[]>('django', '/api/v1/songs/artists', {
  query: { q: newArtistSong.value.artist_name }
})

const artistSuggestions = computed(() => {
  if (responseData.value) {
    return responseData.value.map(artist => ({ label: artist.name, genre: artist.genre }))
  }
})

/**
 * Utilities
 */

/**
 * Function used to split the artist name if the text is
 * in the format "Artist - Song name"
 */
// async function handleSplit() {
//   if (newArtistSong.value.artist_name.includes('-') && newArtistSong.value.artist_name !== '') {
//     const tokens = newArtistSong.value.artist_name.split('-')
//     newArtistSong.value.artist_name = tokens[0].trim()
//     newArtistSong.value.name = tokens[1].trim()
//     await handleSearchExistingArtist()
//   }
// }

// const { currentYear } = useDayJs()
</script>
