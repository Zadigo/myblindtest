<template>
  <section id="list-songs">
    <div class="mx-auto">
      <!-- Header -->
      <volt-card class="mb-2 border-none">
        <template #content>
          <div class="flex items-center gap-2 mb-3 w-full">
            <volt-button @click="handleBack">
              <icon name="fa-solid:arrow-left" /> {{ $t('Back') }}
            </volt-button>

            <div class="ml-auto space-x-2 flex items-center">
              <volt-button @click="getPrevious">
                <icon name="fa-solid:caret-left" />
                {{ $t('Previous') }}
              </volt-button>

              <volt-button @click="getNextPage">
                {{ $t('Next') }}
                <icon name="fa-solid:caret-right" />
              </volt-button>
            </div>
          </div>

          <!-- Search -->
          <volt-input-text v-model="search" type="search" :placeholder="$t('Search artists, songs...')" class="w-6/12 mt-5" />
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
                  <volt-link v-if="artist.wikipedia_page" :href="artist.wikipedia_page" target="_blank" class="mb-5">
                    <icon name="fa6-brands:wikipedia-w" />
                    Page Wikipedia
                  </volt-link>

                  <div v-for="song in artist.song_set" :key="song.id" :aria-label="song.name" class="p-3 rounded-md bg-primary-600 dark:bg-primary-700 dark:text-surface-50 my-1">
                    <div class="inline-flex gap-3 items-center">
                      <span>{{ song.name }}</span>

                      <div class="inline-flex items-center gap-1">
                        <template v-for="i in 5" :key="i">
                          <icon v-if="i <= song.difficulty" name="fa-solid:star" class="dark:text-surface-300" />
                          <icon v-else name="fa-solid:star" class="text-surface-50" />
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

      <div v-else>
        <div class="text-center text-xl bg-primary-100 dark:bg-primary-800 dark:text-primary-50 p-5 rounded-md">
          {{ $t('No songs found') }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useToast } from 'primevue/usetoast'
import type { ArtistSong, BaseApiResponse } from '~/types'

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
apiResult.value = await $fetch<ApiResponse>('/api/v1/songs/by-artists', {
  method: 'get',
  baseURL: useRuntimeConfig().public.apiBaseUrl,
  query: searchParam
})

// Get the previous page
async function getPrevious() {
  if (apiResult.value) {
    searchParam.offset = apiResult.value.previous

    apiResult.value = await $fetch<ApiResponse>('/api/v1/songs/by-artists', {
      method: 'get',
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      query: searchParam
    })
  }
}

// Get the next page
async function getNextPage() {
  if (apiResult.value) {
    searchParam.offset = apiResult.value.next

    apiResult.value = await $fetch<ApiResponse>('/api/v1/songs/by-artists', {
      method: 'get',
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      query: searchParam
    })  
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
  
  try {
    apiResult.value = await $fetch<ApiResponse>('/api/v1/songs/by-artists', {
      method: 'get',
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      query: searchParam
    })
  } catch {
    toast.add({ severity: 'error', summary: 'Error', detail: 'An error occurred while searching for songs.', life: 5000 })
  }
})

/**
 * String
 */

const { plural } = useString()
</script>
