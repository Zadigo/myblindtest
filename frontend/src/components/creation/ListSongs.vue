<template>
  <section class="row">
    <div class="col-sm-12 col-md-6 offset-md-3">
      <v-card class="mb-2">
        <v-card-text>
          <v-btn variant="tonal" @click="emit('back')">
            <FontAwesomeIcon icon="arrow-left" /> Back
          </v-btn>
          
          <v-btn variant="tonal" @click="getPrevious">
            Previous
          </v-btn>

          <v-btn variant="tonal" @click="getNextPage">
            Next
          </v-btn>        
        </v-card-text>
      </v-card>
    </div>

    <div class="col-sm-12 col-md-6 offset-md-3">
      <v-expansion-panels>
        <v-expansion-panel v-for="artist in artists" :key="artist.name">
          <v-expansion-panel-title>
            <div class="row">
              <div class="d-flex justify-content-start align-items-center gap-3">
                <v-avatar :image="artist.avatar" />
                <span>{{ artist.name }}</span>
              </div>
            </div>
          </v-expansion-panel-title>

          <v-expansion-panel-text v-if="byArtist">
            <div class="list-group">
              <div v-for="song in byArtist[artist.name]" :key="song.id" class="list-group-item">
                {{ song.name }}
              </div>
            </div>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>        
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useLimitOffeset } from '@/composables/utils';
import { useAxiosClient } from '@/plugins/client';
import { Song } from '@/types';
import { ref } from 'vue';
import { toast } from 'vue-sonner';

type SongItem = Record<string, Song[]>


interface Artist {
  name: string
  avatar: string
}

interface ApiResponse {
  previous: string
  next: string
  artists: Artist[]
  items: SongItem
}

const emit = defineEmits({
  back() {
    return true
  }
})

const { parser } = useLimitOffeset()
const { client } = useAxiosClient()

const previousLink = ref<string>()
const nextLink = ref<string>()
const artists = ref<Artist[]>([])
const byArtist = ref<SongItem>()

async function getSongs (offset: string | number = 100) {
  try {
    const response = await client.get<ApiResponse>('/songs/by-artists', {
      params: {
        offset
      }
    })

    artists.value = response.data.artists
    byArtist.value = response.data.items

    previousLink.value = response.data.previous
    nextLink.value = response.data.next
  } catch {
    toast.error('Could not get songs')
  }
}

async function getPrevious () {
  if (previousLink.value) {
    const result = parser(previousLink.value)
    getSongs(result.offset)
  }
}


async function getNextPage () {
  if (nextLink.value) {
    const result = parser(nextLink.value)
    getSongs(result.offset)
  }
}

getSongs()
</script>
