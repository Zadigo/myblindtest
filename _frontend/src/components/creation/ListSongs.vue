<template>
  <section id="list">
    <div class="mx-auto w-6/12">
      <!-- Header -->
      <volt-card class="mb-2 border-none">
        <template #content>
          <div class="flex items-center gap-2 mb-3 w-full">
            <volt-button @click="handleBack">
              <VueIcon icon="fa-solid:arrow-left" /> Back
            </volt-button>

            <div class="ml-auto space-x-2 flex items-center">
              <volt-button @click="getPrevious">
                <VueIcon icon="fa-solid:caret-left" />
                Previous
              </volt-button>

              <volt-button @click="getNextPage">
                Next
                <VueIcon icon="fa-solid:caret-right" />
              </volt-button>
            </div>
          </div>

          <volt-input-text v-model="search" type="search" placeholder="Search" />
        </template>
      </volt-card>

      <!-- Songs -->
      <div v-if="apiResult" id="results">
        <volt-card>
          <template #content>
            <volt-accordion>
              <volt-accordion-panel v-for="artist in apiResult.results" :key="artist.name" :value="artist.name">
                <volt-accordion-header>
                  <div class="flex justify-start gap-5 items-center">
                    <volt-avatar :image="artist.spotify_avatar" :alt="artist.name" shape="circle" />

                    <!-- <volt-popover ref="popoverEl">
                      <img :src="artist.spotify_avatar" class="aspect-square object-contain rounded-md">
                    </volt-popover> -->

                    <div class="flex flex-col items-start">
                      <span>{{ artist.name }}</span>
                      <volt-badge variant="secondary" class="mt-2">
                        {{ artist.song_set.length }} {{ plural(artist.song_set, 'song') }}
                      </volt-badge>
                    </div>
                  </div>
                </volt-accordion-header>

                <volt-accordion-content>
                  <div v-for="song in artist.song_set" :key="song.id" :aria-label="song.name" class="p-3 rounded-md bg-primary-600 dark:bg-primary-700 dark:text-surface-50 my-1">
                    <div class="inline-flex gap-3 items-center">
                      <span>{{ song.name }}</span>

                      <div class="inline-flex items-center gap-1">
                        <template v-for="i in 5" :key="i">
                          <vue-icon v-if="i <= song.difficulty" icon="fa-solid:star" class="dark:text-surface-300" />
                          <vue-icon v-else icon="fa-solid:star" class="text-surface-50" />
                        </template>
                      </div>
                    </div>
                  </div>
                </volt-accordion-content>
              </volt-accordion-panel>
            </volt-accordion>
          </template>
        </volt-card>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { ArtistSong, BaseApiResponse } from '@/types'
import { useToast } from 'primevue/usetoast'

const toast = useToast()

interface ApiResponse extends BaseApiResponse<ArtistSong> {
  count: number
}

const emit = defineEmits({
  back() {
    return true
  }
})

const searchParam = useUrlSearchParams('history', {
  initialValue: {
    q: null,
    limit: 100,
    offset: 0,
    v: 'l'
  } as {
    q: string | null
    limit: number
    offset: number
    v: 'l' | 'c'
  }
})

const apiResult = ref<ApiResponse>()

/**
 * Return all the songs in the database
 * @param offset The next offset page to get
 */
const { status, execute, responseData, refresh } = useRequest<ApiResponse>('django', '/api/v1/songs/by-artists', {
  method: 'get',
  query: searchParam
})

await execute()

if (responseData.value) {
  apiResult.value = responseData.value
}

// Get the previous page
async function getPrevious() {
  if (apiResult.value) {
    searchParam.offset = apiResult.value.previous
    await refresh(searchParam)
    apiResult.value = responseData.value
  }
}

// Get the next page
async function getNextPage() {
  if (apiResult.value) {
    searchParam.offset = apiResult.value.next
    await refresh(searchParam)
    apiResult.value = responseData.value
  }
}

// Return to previous component
function handleBack() {
  searchParam.v = 'c'
  emit('back')
}

/**
 * Popover
 */

// const popoverEl = useTemplateRef('popoverEl')

// function showPopover(e: Event) {
//   if (isDefined(popoverEl)) {
//     popoverEl.value.toggle(e)
//   }
// }

/**
 * Lifecycle
 */

onBeforeMount(() => {
  searchParam.v = 'l'
})

/**
 * Search songs
 */

const search = ref<string>('')
const debouncedSearch = debouncedRef(search, 2000)

watch(debouncedSearch, async (newSearch) => {
  searchParam.q = newSearch
  await refresh(searchParam)
  apiResult.value = responseData.value
})

/**
 * String
 */

const { plural } = useString()
</script>
