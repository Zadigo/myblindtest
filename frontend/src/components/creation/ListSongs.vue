<template>
  <section id="list">
    <div class="mx-auto w-6/12">
      <VoltCard class="mb-2 border-none">
        <template #content>
          <div class="flex items-center gap-2 mb-3 w-full">
            <VoltButton @click="handleBack">
              <VueIcon icon="fa-solid:arrow-left" /> Back
            </VoltButton>

            <div class="ml-auto space-x-2 flex items-center">
              <VoltButton @click="getPrevious">
                <VueIcon icon="fa-solid:caret-left" />
                Previous
              </VoltButton>

              <VoltButton @click="getNextPage">
                Next
                <VueIcon icon="fa-solid:caret-right" />
              </VoltButton>
            </div>
          </div>

          <VoltInputText v-model="search" type="search" placeholder="Search" @input="debouncedGetSongs" />
        </template>
      </VoltCard>

      <div v-if="apiResult" id="results">
        <VoltCard>
          <template #content>
            <VoltAccordion>
              <VoltAccordionPanel v-for="artist in apiResult.results" :key="artist.name" :value="artist.name">
                <VoltAccordionHeader>
                  <div class="flex justify-start gap-5 items-center">
                    <VoltAvatar :image="artist.spotify_avatar" :alt="artist.name" @mouseenter="showPopover" />

                    <VoltPopover ref="popoverEl">
                      <img :src="artist.spotify_avatar" class="aspect-square object-contain rounded-md">
                    </VoltPopover>

                    <div class="flex flex-col items-start">
                      <span>{{ artist.name }}</span>
                      <Badge variant="secondary">
                        {{ artist.song_set.length }} {{ plural(artist.song_set, 'song') }}
                      </Badge>
                    </div>
                  </div>
                </VoltAccordionHeader>

                <VoltAccordionContent>
                  <div v-for="song in artist.song_set" :key="song.id" :aria-label="song.name" class="p-3 rounded-md bg-blue-200 my-1">
                    <div class="inline-flex gap-3 items-center">
                      <span>{{ song.name }}</span>

                      <div class="inline-flex items-center gap-1">
                        <template v-for="i in 5" :key="i">
                          <VueIcon v-if="i <= song.difficulty" icon="fa-solid:star" />
                          <VueIcon v-else icon="fa-solid:star" class="text-slate-100" />
                        </template>
                      </div>
                    </div>
                  </div>
                </VoltAccordionContent>
              </VoltAccordionPanel>
            </VoltAccordion>
          </template>
        </VoltCard>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { ArtistSong } from '@/types'
import { toast } from 'vue-sonner'

// TODO: Refactor the types
// for this endpoint because it
// is very confusing
interface ApiResponse {
  count: number
  next: number
  previous: number
  results: ArtistSong[]
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

const search = ref<string>('')
const apiResult = ref<ApiResponse>()

/**
 * Return all the songs in the database
 *
 * @param offset The next offset page to get
 */
const { status, execute, responseData, refresh } = useRequest<ApiResponse>('django', '/api/v1/songs/by-artists', {
  method: 'get',
  query: searchParam
})

await execute()

if (responseData.value) {
  // searchParam.q = search.value
  // searchParam.offset = offset
  apiResult.value = responseData.value
}

/**
 * Get the previous page
 */
async function getPrevious() {
  if (apiResult.value) {
    searchParam.offset = apiResult.value.previous
    await execute()
  }
}

/**
 * Get the next page
 */
async function getNextPage() {
  if (apiResult.value) {
    searchParam.offset = apiResult.value.next
    await execute()
  }
}

/**
 * Return to previous component
 */
function handleBack() {
  searchParam.v = 'c'
  emit('back')
}

/**
 * Popover
 */

const popoverEl = useTemplateRef('popoverEl')

function showPopover(e: Event) {
  if (isDefined(popoverEl)) {
    popoverEl.value.toggle(e)
  }
}

onBeforeMount(() => {
  searchParam.v = 'l'
})

const debouncedGetSongs = useDebounceFn(async () => await refresh({ q: searchParam.q }), 2000)

/**
 * String
 */

const { plural } = useString()
</script>
