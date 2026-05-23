<template>
  <volt-container class="h-screen" size="md">
    <div class="space-y-2">
      <volt-card>
        <template #content>
          <h1 class="font-bold text-3xl">
            {{ $t('Create songs') }}
          </h1>

          <p>{{ $t('Create new songs for brand', { brand: 'MyBlindTest' }) }}</p>
        </template>
      </volt-card>
  
      <!-- Songs -->
      <suspense v-if="showSongs">
        <template #default>
          <async-list-songs @back="handleBack" />
        </template>
  
        <template #fallback>
          <section id="list">
            <div class="space-y-2">
              <volt-skeleton v-for="i in 10" :key="i" height="120px" width="auto" />
            </div>
          </section>
        </template>
      </suspense>
  
      <!-- Creation -->
      <div v-else id="song-creation">
        <volt-card class="border-none">
          <template #content>
            <client-only>
              <div v-auto-animate>
                <template v-for="(_, idx) in blocks" :key="idx">
                  <creation-create-block :index="idx" />
                  <volt-divider v-if="blocks.length > 1 && idx !== blocks.length - 1" class="my-5" />
                </template>
              </div>
            </client-only>
          </template>
  
          <template #footer>
            <div class="space-x-2">
              <volt-button class="ms-auto" @click="addBlock">
                <icon name="fa-solid:plus" />{{ $t('Add block') }}
              </volt-button>
  
              <volt-button @click="save">
                <icon name="fa-solid:save" />
                {{ $t('Save') }}
              </volt-button>
  
              <volt-button @click="showSongs=true">
                <icon name="fa-solid:table" />
                {{ $t('Songs') }}
              </volt-button>
            </div>
          </template>
        </volt-card>
      </div>
    </div>
  </volt-container>
</template>

<script setup lang="ts">
const AsyncListSongs = defineAsyncComponent({
  loader: async () => import('~/components/creation/ListSongs.vue'),
  timeout: 20000
})

/**
 * URL search param
 * - c: Create
 * - l: List of songs
 */

const searchParam = useUrlSearchParams('history', {
  initialValue: {
    v: 'c'
  }
})

function handleBack() {
  searchParam.v = 'c'
  showSongs.value = false
}

/**
 * Autocompletion
 */

const { showSongs, genres } = useAutocompleteGenres()
const { blocks, addBlock, save } = useEditSong()

provide('genres', genres)

onMounted(async () => {
  if (searchParam.v === 'l') {
    showSongs.value = true
  }
})

/**
 * SEO
 */

const { locale } = useI18n()

const titles = {
  en: 'Create songs',
  fr: 'Créer des chansons',
}

const descriptions = {
  en: 'Create new songs for MyBlindTest',
  fr: 'Créer de nouvelles chansons pour MyBlindTest',
}

useHead({
  title: titles[locale.value],
  meta: [
    {
      name: 'description',
      content: descriptions[locale.value]
    }
  ]
})
</script>
