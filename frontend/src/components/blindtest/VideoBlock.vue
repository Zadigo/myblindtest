<template>
  <div class="video">
    <div v-if="showWheel" class="card">
      <FortuneWheel ref="wheel" v-model="selectedGenre" :middle-circle="true" :data="data" @click="spinWheel" @done="spinDone" />
    </div>

    <div v-else class="card shadow-sm">
      <div class="card-header border-bottom-0">
        <div class="row">
          <div class="col-12 d-flex justify-content-between">
            <div class="col-auto">
              <div class="mb-1 badge fs-5 text-bg-primary p-2">
                {{ songsStore.cache.currentStep }}/-
              </div>
            </div>

            <div class="col-auto">
              <v-btn variant="tonal" color="dark" class="me-2" rounded @click="showWheel=!showWheel">
                <FontAwesomeIcon icon="bolt" />
              </v-btn>

              <v-btn variant="tonal" color="dark" rounded @click="emit('game:settings')">
                <FontAwesomeIcon icon="cog" />
              </v-btn>
            </div>
          </div>

          <div class="col-12">
            <h4 v-if="currentSong" class="h5 mt-4 mb-1">
              {{ currentSong.name }}
            </h4>

            <div v-if="currentSong" class=" mb-1 fw-light d-flex align-items-center gap-2">
              <span>{{ currentSong.artist }}</span>
              <span class="badge text-bg-secondary">
                {{ currentSong.genre }}
              </span>
            </div>
            
            <v-rating v-if="currentSong" :length="5" :model-value="currentSong.difficulty" :size="22" color="blue-darken-1" readonly />
          </div>
        </div>
      </div>

      <div v-if="currentSong" class="card-body">
        <iframe :src="currentSong.youtube" width="400" height="200" title="Sinéad O&#39;Connor - Nothing Compares 2 U (Official Music Video) [HD]" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" />
      </div>

      <div v-else class="text-center">
        <div class="p-5">
          <span class="loader-12" />
        </div>
      </div>

      <div class="card-footer d-flex justify-content-between align-items-center">
        <div class="actions">
          <v-btn v-if="isStarted" variant="tonal" @click="handleStop">
            <FontAwesomeIcon icon="stop" class="me-2" /> Stop
          </v-btn>

          <v-btn v-else variant="tonal" @click="handleStart">
            <FontAwesomeIcon icon="play" class="me-2" /> Start
          </v-btn>
        </div>

        <div class="d-flex gap-1">
          <v-btn :disabled="!isStarted" variant="tonal" @click="handleNextSong">
            <FontAwesomeIcon icon="close" class="me-2" /> Wrong answer
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { getBaseUrl } from '@/plugins/client';
import { useSongs } from '@/stores/songs';
import type { Song } from '@/types';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useWebSocket } from '@vueuse/core';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import { toast } from 'vue-sonner';
import { wheelDetaults } from '@/data/defaults'
import type { Data } from 'vue3-fortune-wheel';
// https://github.com/joffreyBerrier/vue-fortune-wheel
import { FortuneWheel } from 'vue3-fortune-wheel';

interface WebsocketMessage {
  type: string,
  exclude?: number[]
  genre?: string
}

// import z from 'zod'

const emit = defineEmits({
  'game:settings' () {
    return true
  }
})

const songsStore = useSongs()
const { selectedSongs, isStarted, currentSong } = storeToRefs(songsStore)

const showWheel = ref(false)
const selectedGenre = ref(0)
const wheel = ref<InstanceType<typeof FortuneWheel> | null>(null)
const data = ref<Data[]>(wheelDetaults)

const ws = useWebSocket(getBaseUrl('/ws/songs', null, true), {
  immediate: false,
  onConnected() {
    isStarted.value = true
  },
  onMessage() {
    const data = JSON.parse(ws.data.value)

    if (data.type === 'get.song') {
      if (songsStore.cache) {
        songsStore.cache.songs.push(data.data as Song)
      }
    }
    
    if (data.type === 'next.song') {
      if (songsStore.cache) {
        const existingSong = songsStore.cache.songs.filter(x => x.id === data.data.id)

        if (existingSong.length > 0) {
          toast.error('Song already played')
        } else {
          songsStore.cache.songs.push(data.data as Song)
        }
      }
    }
  },
  onDisconnected() {
    isStarted.value = false
    toast.error('Disconnected')
  },
  onError() {
    toast.error('Websocket error')
  }
})

// Function that selects a random index and then
// spins the wheel in order to select the genre
function spinWheel () {
  selectedGenre.value = Math.floor(Math.random() * wheelDetaults.length) + 1
  wheel.value?.spin()
}

function sendMessage <T extends WebsocketMessage>(data: T) {
  return JSON.stringify(data)
}

// Function that gets called once the
// spinning has finished
function spinDone (result: Data) {
  showWheel.value = false
  ws.send(sendMessage({
    type: 'next-song',
    genre: result.value
  }))
}

// Returns the next song by excluding
// those that were already played
function handleNextSong () {
  ws.send(sendMessage({ 
    type: 'next.song', 
    exclude: songsStore.cache.songs.map(x => x.id)
  }))
  
  songsStore.cache.currentStep += 1
}

// Starts the game
function handleStart () {
  ws.open()
  ws.send(sendMessage({ type: 'get.song' }))
  toast.success('Started blind test')
}

// Stops the game
function handleStop () {
  ws.close()
  toast.success('Stopped blind test')

  if (songsStore.cache) {
    selectedSongs.value = []
    songsStore.cache.songs = []

    songsStore.cache.teams.forEach(x => {
      x.score = 0
    })
    songsStore.cache.currentStep = 0
  }
}

defineExpose({
  handleNextSong
})
</script>
