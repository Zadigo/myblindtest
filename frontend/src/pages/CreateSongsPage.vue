<template>
  <section class="my-5">
    <div class="col-sm-12 col-md-8 offset-md-2">
      <div class="card shadow-sm">
        <TransitionGroup name="opacity">
          <template v-for="(block, i) in blocks" :key="i">
            <CreateBlock :block="block" :index="i" />
            <hr v-if="blocks.length > 1 && i !== blocks.length - 1" class="my-5">
          </template>
        </TransitionGroup>


        <div class="card-body d-flex gap-2">
          <v-btn variant="tonal" color="dark" @click="handleAddBlock">
            <FontAwesomeIcon class="me-2" icon="plus" />Add block
          </v-btn>
          
          <v-btn variant="tonal" color="dark" @click="handleSave">
            Save
          </v-btn>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useAxiosClient } from '@/plugins/client';
import { CreateData } from '@/types';
import { onMounted, provide, ref } from 'vue';
import { toast } from 'vue-sonner';
import { useLocalStorage } from '@vueuse/core';

import CreateBlock from '@/components/creation/CreateBlock.vue';
import { addNewSongData } from '@/data/defaults';

const blocks = ref<CreateData[]>([ addNewSongData ])

const { client } = useAxiosClient()

const genres = useLocalStorage<string[]>('genres', null, {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    }
  }
})

async function handleSave () {
  try {
    client.post('/songs/create', blocks.value)
    blocks.value = [ addNewSongData ]
  } catch {
    toast.error('Could not create songs')
  }
}

async function handleGetGenres () {
  try {
    if (genres.value) {
      if (genres.value.length === 0) {
        const response = await client.get<string[]>('/songs/genres')
        genres.value = response.data
      }
    }
  } catch {
    toast.error('Failed to get genres')
  }
}

function handleAddBlock () {
  blocks.value.push(addNewSongData)
}

provide('genres', genres)

onMounted(async () => {
  await handleGetGenres()
})
</script>
