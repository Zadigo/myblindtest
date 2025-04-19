<template>
  <section class="row">
    <div class="col-sm-12 col-md-6 offset-md-3">
      <v-card class="mb-2">
        <v-card-text>
          <div class="d-flex gap-2 mb-3">
            <v-btn variant="tonal" @click="emit('back')">
              <FontAwesomeIcon icon="arrow-left" /> Back
            </v-btn>

            <v-btn variant="tonal" @click="getPrevious">
              Previous
            </v-btn>

            <v-btn variant="tonal" @click="getNextPage">
              Next
            </v-btn>
          </div>

          <v-text-field v-model="search" variant="solo-filled" type="search" placeholder="Search" flat @input="debouncedGetSongs" />
        </v-card-text>
      </v-card>
    </div>

    <div v-if="apiResult" class="col-sm-12 col-md-6 offset-md-3">
      <v-expansion-panels>
        <v-expansion-panel v-for="artist in apiResult.results" :key="artist.name">
          <v-expansion-panel-title>
            <div class="row">
              <div class="d-flex justify-content-start align-items-center gap-3">
                <v-avatar>
                  <v-img :src="artist.spotify_avatar" :alt="artist.name" />
                </v-avatar>
                <span>{{ artist.name }}</span>
                <span class="badge text-bg-secondary">{{ artist.song_set.length }} {{ plural(artist.song_set, 'song') }}</span>
              </div>
            </div>
          </v-expansion-panel-title>

          <v-expansion-panel-text>
            <div class="list-group">
              <div v-for="song in artist.song_set" :key="song.id" :aria-label="song.name" class="list-group-item p-3 d-flex justify-content-between align-items-center">
                <span>{{ song.name }}</span>
                <v-rating :size="22" :length="song.difficulty" model-value="5" readonly />
              </div>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useDebounce, useLimitOffeset, useString } from '@/composables/utils'
import { useAxiosClient } from '@/plugins/client'
import { ArtistSong } from '@/types'
import { ref } from 'vue'
import { toast } from 'vue-sonner'

// TODO: Refactor the types
// for this endpoint because it
// is very confusing
interface ApiResponse {
  count: number
  next: string
  previous: string
  results: ArtistSong[]
}

const emit = defineEmits({
  back() {
    return true
  }
})

const { plural } = useString()
const { parser } = useLimitOffeset()
const { client } = useAxiosClient()
const { debounce } = useDebounce()

const search = ref<string>('')
const previousLink = ref<string>()
const nextLink = ref<string>()
const apiResult = ref<ApiResponse>()

async function getSongs(offset: string | number = 0) {
  try {
    const response = await client.get<ApiResponse>('/songs/by-artists', {
      params: {
        offset,
        q: search.value
      }
    })

    apiResult.value = response.data

    previousLink.value = response.data.previous
    nextLink.value = response.data.next
  } catch {
    toast.error('Could not get songs')
  }
}

const debouncedGetSongs = debounce(getSongs, 4000)

async function getPrevious() {
  if (previousLink.value) {
    const result = parser(previousLink.value)
    getSongs(result.offset)
  }
}

async function getNextPage() {
  if (nextLink.value) {
    const result = parser(nextLink.value)
    getSongs(result.offset)
  }
}

getSongs()
</script>
