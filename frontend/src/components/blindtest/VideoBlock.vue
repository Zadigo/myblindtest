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

                <v-btn :disabled="!gameStarted" variant="tonal" color="dark" class="me-2" rounded @click="showWheel=!showWheel">
                  <FontAwesomeIcon icon="bolt" />
                </v-btn>

                <!-- <v-btn variant="tonal" color="dark" rounded @click="emit('game:settings')">
                  <FontAwesomeIcon icon="cog" />
                </v-btn> -->
              </div>
            </div>

            <div class="col-12">
              <h4 v-if="currentSong" class="h5 mt-4 mb-1">
                {{ currentSong.name }}
              </h4>

              <div v-if="currentSong" class=" mb-1 fw-light d-flex align-items-center gap-2">
                <span>{{ currentSong.artist.name }}</span>
                <span class="badge text-bg-secondary">
                  {{ currentSong.genre }}
                </span>
              </div>
              
              <v-rating v-if="currentSong" :length="5" :model-value="currentSong.difficulty" :size="22" color="blue-darken-1" readonly />
            </div>
          </div>
        </div>

        <div v-if="currentSong" class="card-body d-flex justify-content-center">
          <iframe :src="currentSong.youtube" width="400" height="200" title="Sinéad O&#39;Connor - Nothing Compares 2 U (Official Music Video) [HD]" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" />
        </div>

        <div v-else class="text-center">
          <div class="p-5">
            <span class="loader-12" />
          </div>
        </div>

        <div class="card-footer d-flex justify-content-between align-items-center">
          <div class="actions">
            <v-btn v-if="gameStarted" variant="tonal" @click="handleStop">
              <FontAwesomeIcon icon="stop" class="me-2" /> Stop
            </v-btn>

            <v-btn v-else variant="tonal" @click="handleStart">
              <FontAwesomeIcon icon="play" class="me-2" /> Start
            </v-btn>
          </div>

          <div class="d-flex gap-1">
            <v-btn :disabled="!gameStarted" variant="tonal" @click="handleIncorrectAnswer">
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
import type { MatchedElement, Song, WebsocketBlindTestMessage } from '@/types';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useLocalStorage, useWebSocket } from '@vueuse/core';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import { toast } from 'vue-sonner';
import { RandomizerData } from '../randomizer';

import GenreRandomizer from '../randomizer/GenreRandomizer.vue';
import { useWebsocketUtilities } from '@/composables/utils';


// import z from 'zod'

const songsStore = useSongs()
const { gameStarted, currentSong } = storeToRefs(songsStore)
const { sendMessage, parseMessage } = useWebsocketUtilities()

const connectionToken = useLocalStorage<string | null | undefined>('connectionToken', null)

const showWheel = ref(false)
const randomizerEl = ref<HTMLElement>()

const ws = useWebSocket(getBaseUrl('/ws/songs', null, true), {
  immediate: false,
  onConnected() {
    const settings = songsStore.cache.settings

    ws.send(sendMessage<WebsocketBlindTestMessage>({
      action: 'start_game',
      cache: songsStore.cache,
      // TODO: Just use and send all the cache
      settings: {
        point_value: settings.pointValue,
        game_difficulty: settings.difficultyLevel,
        genre: settings.songType,
        difficulty_bonus: settings.songDifficultyBonus,
        // TODO: speed_bonus
        time_bonus: settings.speedBonus,
        number_of_rounds: settings.rounds,
        solo_mode: settings.soloMode,
        admin_plays: settings.adminPlays
      }
    }))

    toast.success('Info', {
      description: 'Started blind test'
    })
  },
  onMessage() {
    const data = parseMessage<WebsocketBlindTestMessage>(ws.data.value)

    switch (data.action) {
      case 'game_started':
        gameStarted.value = true
        break

      case 'song_new':
        songsStore.cache.songs.push(data.song as Song)
        break

      case 'timer_tick':
        break

      case 'guess_correct':
        // When we receive a message that the guess was
        // correct by the given team, update the score
        songsStore.cache.teams[data.team_id].score = data.points
        break

      case 'song_skipped':
        break

      case 'connection_token':
        connectionToken.value = data.token
        break

      case 'randomize_genre':
        songsStore.cache.songs.push(data.song as Song)
        break

      case 'device_connected':
        ws.send(sendMessage<WebsocketBlindTestMessage>({
          action: 'update_device_cache',
          cache: songsStore.cache
        }))
        toast.success('Device', {
          description: 'Projecton device connected'
        })
        break
        
      case 'device_disconnected':
        toast.success('Device', {
          description: 'Projecton device disconnected'
        })
        break

      case 'error':
        toast.error('Error', {
          description: data.error
        })
        break

      default:
        break
    }
  },
  onDisconnected() {
    gameStarted.value = false
    toast.error('Error', {
      description: 'Game has been disconnected'
    })
  },
  onError() {
    toast.error('Error', {
      description: 'An error has occured'
    })
  }
})

// Function that gets called once the
// spinning has finished
function randomizerComplete (value: string | undefined | RandomizerData) {
  if (value) {
    setTimeout(() => {
      showWheel.value = false

      ws.send(sendMessage<WebsocketBlindTestMessage>({
        action: 'randomize_genre',
        temporary_genre: value
      }))
    }, 3000)
  }
}

function handleFinalize() {
  songsStore.cache.currentStep += 1
}

// Returns the next song by excluding
// those that were already played
function handleIncorrectAnswer () {
  ws.send(sendMessage<WebsocketBlindTestMessage>({ action: 'skip_song' }))
  handleFinalize()
}

// Proxy function that can be used by parent elements
// to trigger a websocket message on the team guess
function handleCorrectAnswer(teamId: number, match: MatchedElement) {
  let title_match: boolean = true
  let artist_match: boolean = true

  if (match === 'Title') {
    title_match = true
    artist_match = false
  }

  if (match === 'Artist') {
    title_match = false
    artist_match = true
  }

  ws.send(sendMessage<WebsocketBlindTestMessage>({
    action: 'submit_guess',
    team_id: teamId,
    title_match,
    artist_match
  }))

  handleFinalize()
}

// Starts the game
function handleStart () {
  ws.open()
}

// Stops the game
function handleStop () {
  ws.close()
  toast.success('Stopped blind test')

  if (songsStore.cache) {
    songsStore.cache.songs = []
    songsStore.correctAnswers = []

    songsStore.cache.teams.forEach(x => {
      x.score = 0
    })
    songsStore.cache.currentStep = 0
  }
}

defineExpose({
  handleCorrectAnswer,
  handleIncorrectAnswer
})
</script>
