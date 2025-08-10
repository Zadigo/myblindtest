<template>
  <section class="my-5 px-10">
    <Suspense v-if="showSongs">
      <template #default>
        <AsyncListSongs @back="showSongs=false" />
      </template>

      <template #fallback>
        <section id="list">
          <div class="mx-auto w-6/12">
            <VoltSkeleton class="w-[200px] h-[200px]" />
          </div>
        </section>
      </template>
    </Suspense>

    <div v-else class="w-6/12 mx-auto">
      <VoltCard class="border-none">
        <template #content>
          <TransitionGroup name="opacity">
            <template v-for="(block, i) in blocks" :key="i">
              <CreateBlock :block="block" :index="i" @delete:block="deleteBlock" />
              <VoltDivider v-if="blocks.length > 1 && i !== blocks.length - 1" class="my-5" />
            </template>
          </TransitionGroup>
        </template>

        <template #footer>
          <div class="space-x-2">
            <VoltButton class="ms-auto" @click="addBlock">
              <VueIcon icon="fa-solid:plus" />Add block
            </VoltButton>

            <VoltButton @click="save">
              <VueIcon icon="fa-solid:save" />
              Save
            </VoltButton>

            <VoltButton @click="showSongs=true">
              <VueIcon icon="fa-solid:table" />
              Songs
            </VoltButton>
          </div>
        </template>
      </VoltCard>
    </div>
  </section>
</template>

<script setup lang="ts">
const AsyncListSongs = defineAsyncComponent({
  loader: async () => import('@/components/creation/ListSongs.vue'),
  timeout: 20000
})

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

const { showSongs, genres } = useGetGenres()
const { blocks, addBlock, save, deleteBlock } = useEditSong()

provide('genres', genres)

onMounted(async () => {
  if (searchParam.v === 'l') {
    showSongs.value = true
  }
})
</script>
