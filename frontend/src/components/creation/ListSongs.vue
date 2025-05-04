<template>
  <section id="list">
    <div class="mx-auto w-6/12">
      <Card class="mb-2 border-none">
        <CardContent>
          <div class="flex gap-2 mb-3 w-full">
            <Button @click="emit('back')">
              <Icon icon="fa-solid:arrow-left" /> Back
            </Button>

            <div class="self-end">
              <Button @click="getPrevious">
                Previous
              </Button>

              <Button @click="getNextPage">
                Next
              </Button>
            </div>
          </div>

          <Input v-model="search" type="search" placeholder="Search" @input="debouncedGetSongs" />
        </CardContent>
      </Card>

      <div v-if="apiResult" id="results">
        <Accordion type="single" collapsible>
          <AccordionItem v-for="artist in apiResult.results" :key="artist.name" :value="artist.name">
            <AccordionTrigger>
              <div class="flex justify-start gap-5 items-center">
                <HoverCard class="border-none shadow-lg">
                  <HoverCardTrigger>
                    <Avatar>
                      <AvatarImage :src="artist.spotify_avatar" :alt="artist.name" />
                      <AvatarFallback>{{ artist.name }}</AvatarFallback>
                    </Avatar>
                  </HoverCardTrigger>

                  <HoverCardContent>
                    <img :src="artist.spotify_avatar" class="aspect-square object-contain rounded-md">
                  </HoverCardContent>
                </HoverCard>

                <div class="flex flex-col items-start">
                  <span>{{ artist.name }}</span>
                  <Badge variant="secondary">
                    {{ artist.song_set.length }} {{ plural(artist.song_set, 'song') }}
                  </Badge>
                </div>
              </div>
            </AccordionTrigger>
            <AccordionContent>
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
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useDebounce, useLimitOffeset, useString } from '@/composables/utils'
import { ArtistSong } from '@/types'
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
const searchParam = useUrlSearchParams('history', {
  initialValue: {
    q: null,
    limit: 100,
    offset: 0
  } as {
    q: string | null
    limit: number
    offset: number
  }
})

const search = ref<string>('')
const previousLink = ref<string>()
const nextLink = ref<string>()
const apiResult = ref<ApiResponse>()

/**
 * 
 * @param offset The next offset page to get
 */
async function getSongs(offset: string | number = 0) {
  try {
    const response = await client.get<ApiResponse>('/api/v1/songs/by-artists', {
      params: {
        offset,
        q: search.value
      }
    })

    searchParam.q = search.value
    searchParam.offset = offset
    apiResult.value = response.data

    previousLink.value = response.data.previous
    nextLink.value = response.data.next
  } catch {
    toast.error('Could not get songs')
  }
}

const debouncedGetSongs = debounce(getSongs, 4000)

/**
 * Get the previous page
 */
async function getPrevious() {
  if (previousLink.value) {
    const result = parser(previousLink.value)
    getSongs(result.offset)
  }
}

/**
 * Get the next page
 */
async function getNextPage() {
  if (nextLink.value) {
    const result = parser(nextLink.value)
    getSongs(result.offset)
  }
}

await getSongs()
</script>
