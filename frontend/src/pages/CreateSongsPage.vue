<template>
  <section class="my-5 px-10 h-auto">
    <suspense v-if="showSongs">
      <template #default>
        <async-list-songs @back="handleBack" />
      </template>

      <template #fallback>
        <section id="list">
          <div class="mx-auto w-6/12 space-y-2">
            <volt-skeleton v-for="i in 10" :key="i" height="120px" width="600px" />
          </div>
        </section>
      </template>
    </suspense>

    <div v-else class="w-6/12 mx-auto">
      <volt-card class="border-none">
        <template #content>
          <transition-group name="opacity">
            <template v-for="(block, i) in blocks" :key="i">
              <create-block :block="block" :index="i" @delete:block="deleteBlock" />
              <volt-divider v-if="blocks.length > 1 && i !== blocks.length - 1" class="my-5" />
            </template>
          </transition-group>
        </template>

        <template #footer>
          <div class="space-x-2">
            <volt-button class="ms-auto" @click="addBlock">
              <vue-icon icon="fa-solid:plus" />Add block
            </volt-button>

            <volt-button @click="save">
              <vue-icon icon="fa-solid:save" />
              Save
            </volt-button>

            <volt-button @click="showSongs=true">
              <vue-icon icon="fa-solid:table" />
              Songs
            </volt-button>
          </div>
        </template>
      </volt-card>
    </div>
  </section>
</template>

<script setup lang="ts">
const AsyncListSongs = defineAsyncComponent({
  loader: async () => import('@/components/creation/ListSongs.vue'),
  timeout: 20000
})

/**
 * Actions
 */

/**
 * c: Create
 * l: List of songs
 */
const searchParam = useUrlSearchParams('history', {
  initialValue: {
    v: 'c'
  } as {
    v: 'l' | 'c'
  }
})

function handleBack() {
  searchParam.v = 'c'
  showSongs.value = false
}

/**
 * Genres
 */

const { showSongs, genres } = useGetGenres()
const { blocks, addBlock, save, deleteBlock } = useEditSong()

provide('genres', genres)

onMounted(async () => {
  if (searchParam.v === 'l') {
    showSongs.value = true
  }
})

/**
 * SEO
 */

useHead({
  title: 'Create songs',
  meta: [
    {
      name: 'description',
      content: 'Create new songs for MyBlindTest'
    }
  ]
})
</script>
