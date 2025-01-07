<template>
  <div class="video">
    <Transition mode="out-in" name="animate__animated" enter-active-class="animate__animated animate__fadeInDown" leave-active-class="animate__animated animate__fadeOutDown">
      <div v-if="showWheel" class="card">
        <GenreRandomizer ref="randomizerEl" :items="wheelDetaults" @completed="randomizerComplete" />
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
                <v-btn :to="{ name: 'home' }" variant="tonal" color="dark" class="me-2" rounded>
                  <FontAwesomeIcon icon="home" />
                </v-btn>

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
    </Transition>
  </div>
</template>

<script lang="ts" setup>
import { wheelDetaults } from '@/data/defaults';
import { getBaseUrl } from '@/plugins/client';
import { useSongs } from '@/stores/songs';
import type { DifficultyLevels, Song, SongGenres } from '@/types';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useWebSocket } from '@vueuse/core';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import { toast } from 'vue-sonner';
import { RandomizerData } from '../randomizer';

import GenreRandomizer from '../randomizer/GenreRandomizer.vue';

interface WebsocketMessage {
  type: string,
  exclude?: number[]
  game_difficulty?: DifficultyLevels
  genre?: SongGenres
}

// import z from 'zod'

const emit = defineEmits({
  'game:settings' () {
    return true
  }
})

const songsStore = useSongs()
const { selectedSongs, isStarted, currentSong, cache } = storeToRefs(songsStore)

const randomizerEl = ref<HTMLElement>()
const gameStarted = ref(false)
const showWheel = ref(false)

const ws = useWebSocket(getBaseUrl('/ws/songs', null, true), {
  immediate: false,
  onConnected() {
    isStarted.value = true
    toast.success('Started blind test')
  },
  onMessage() {
    const data = JSON.parse(ws.data.value)

    if (data.type === 'start.game') {
      gameStarted.value = true
    }

    if (data.type === 'connection.token') {
      // Do something
    }

    if (data.type === 'get.song') {
      if (songsStore.cache) {
        const existingSong = songsStore.cache.songs.filter(x => x.id === data.song.id)

        if (existingSong.length > 0) {
          toast.error('Song already played')
        } else {
          songsStore.cache.songs.push(data.song as Song)
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


function sendMessage <T extends WebsocketMessage>(data: T) {
  return JSON.stringify(data)
}

// Function that gets called once the
// spinning has finished
function randomizerComplete (value: string | undefined | RandomizerData) {
  if (value) {
    setTimeout(() => {
      showWheel.value = false

      ws.send(sendMessage({
        type: 'get.song.randomizer',
        exclude: cache.value.songs.map(x => x.id),
        genre: value
      }))
    }, 5000)
  }
}

// Returns the next song by excluding
// those that were already played
function handleNextSong () {
  ws.send(sendMessage({ 
    type: 'get.song', 
    exclude: songsStore.cache.songs.map(x => x.id)
  }))
  
  songsStore.cache.currentStep += 1
}

// Starts the game
function handleStart () {
  ws.open()

  if (cache.value) {
    ws.send(sendMessage({
      type: 'start.game',
      game_difficulty: cache.value.settings.difficultyLevel,
      genre: cache.value.settings.songType
    }))

    ws.send(sendMessage({
      type: 'get.song',
      exclude: []
    }))
  }
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
