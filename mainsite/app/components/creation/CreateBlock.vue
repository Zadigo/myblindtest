<template>
  <div :data-id="index" class="space-y-2 mb-10">
    <div class="flex justify-end mb-5">
      <volt-secondary-button v-if="index > 0" rounded @click="() => deleteBlock(index)">
        <icon name="fa-solid:trash" />
      </volt-secondary-button>
    </div>

    <form v-if="newArtistSong" class="space-y-2" @submit.prevent>
      <div class="grid grid-cols-3 gap-2">
        <volt-input-text v-model="newArtistSong.name" :placeholder="$t('Song name')" />
        <volt-autocomplete v-model="newArtistSong.genre" :suggestions="filteredGenres" :virtual-scroller-options="{ itemSize: 50 }" :placeholder="$t('Genre')" option-label="label" option-group-children="items" option-group-label="category" dropdown @complete="searchGenreComplete" />
        <volt-input-number v-model.number="newArtistSong.year" :placeholder="$t('Year')" />
      </div>

      <div class="grid grid-cols-3 gap-2">
        <volt-input-number v-model="newArtistSong.difficulty" :min="1" :max="5" :placeholder="$t('Difficulty')" />
        <volt-autocomplete v-model="newArtistSong.artist_name" :suggestions="artistSuggestions" :virtual-scroller-options="{ itemSize: 50 }" :placeholder="$t('Artist name')" option-label="label" dropdown @complete="() => searchArtists()" />
        <volt-input-text v-model="youtubeUrl" placeholder="Hzu-GygG6zs, https://www.youtube.com/watch?v=Hzu-GygG6zs..." />
        {{ newArtistSong.youtube_id }}
      </div>

      <div class="space-y-2">
        <volt-label label-for="is-group" :label="$t('Is group?')">
          <volt-toggle-switch v-model="newArtistSong.is_group" id="is-group" />
        </volt-label>

        <volt-input-text type="url" v-model="newArtistSong.wikipedia_page" :placeholder="$t('Wikipedia page')" class="w-6/12" />
      </div>
    </form>
  </div>
</template>

<script lang="ts" setup>
import type { SearchedGenreApiResponse } from '@/composables'
import type { Artist } from '~/types'

const defaultProps = withDefaults(defineProps<{ index?: number }>(), {
  index: 0
})

/**
 * Genres suggestions
 */

interface SearchEvent extends Event {
  query: string
}

const injectedGenres = inject<Ref<SearchedGenreApiResponse[]> | undefined>('genres')
const filteredGenres = ref<SearchedGenreApiResponse[]>([])

// Callback function for VoltAutocomplete component
// to filter genres based on user input
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
 * Edit block
 */

const { deleteBlock, getCurrentBlock } = useEditSong()
const newArtistSong = getCurrentBlock(defaultProps.index)
const _artistName = computed(() => {
  if (isDefined(newArtistSong)) {
    return typeof newArtistSong.value.artist_name === 'string' ? newArtistSong.value.artist_name : newArtistSong.value.artist_name.label
  } else {
    return ''
  }
})

/**
 * Artists suggestions
 */

const { responseData, execute: searchArtists } = useRequest<Artist[]>('django', '/api/v1/songs/artists', {
  query: { q: _artistName }
})

const artistSuggestions = computed(() => {
  if (responseData.value) {
    return responseData.value.map(artist => ({ label: artist.name, genre: artist.genre }))
  }
})

/**
 * Utilities
 */

const youtubeUrl = computed({
  get: () => newArtistSong.value?.youtube_id,
  set: (value: string) => {
    if (isDefined(newArtistSong)) {
      if (value.includes('https://www.youtube.com/watch')) {
        const url = new URL(value)
        const videoId = url.searchParams.get('v')
        newArtistSong.value.youtube_id = videoId ? videoId : value
      } else {
        newArtistSong.value.youtube_id = value
      }
    }
  }
})
</script>
