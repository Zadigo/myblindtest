<template>
  <div class="absolute my-10 left-2/6 w-4/12">
    <Card class="border-none shadow-md">
      <CardHeader>
        <div class="flex justify-between align-center">
          <div v-if="currentSong">
            <p class="font-bold">
              {{ currentSong.name }} <span class="font-semibold">({{ currentSong.artist.name }})</span>
            </p>

            <div class="inline-flex gap-1 my-2">
              <template v-for="i in 5" :key="i">
                <VueIcon v-if="i <= currentSong.difficulty" icon="fa-solid:star" />
                <VueIcon v-else icon="fa-solid:star" class="text-slate-50" />
              </template>
            </div>

            <div>
              <Badge variant="default">
                {{ currentSong.genre }}
              </Badge>
            </div>
          </div>

          <div class="flex justify-end gap-2">
            <Button variant="outline">
              <VueIcon icon="fa-solid:home" size="15" />
            </Button>

            <Button variant="outline" @click="showWheel=!showWheel">
              <VueIcon icon="fa-solid:bolt" size="15" />
            </Button>
          </div>
        </div>
      </CardHeader>

      <!-- Video -->
      <CardContent>
        <p class="font-bold mb-3">
          {{ songsStore.cache.currentStep }}/-
        </p>

        <div id="video-wrapper" class="rounded-md overflow-hidden flex justify-center items-center max-w-full">
          <iframe v-if="gameStarted && currentSong" :src="songsStore.currentSong.youtube" :title="songsStore.currentSong.artist.name" class="max-w-full h-auto block" width="400" height="200" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" />
          <Spinner v-else name="loader-4" />
        </div>
      </CardContent>

      <!-- Wheel -->
      <Transition mode="out-in" name="animate__animated" enter-active-class="animate__animated animate__fadeInDown" leave-active-class="animate__animated animate__fadeOutDown">
        <CardContent v-if="showWheel">
          <GenreRandomizer ref="randomizerEl" :items="wheelDetaults" @completed="randomizerComplete" />
        </CardContent>
      </Transition>

      <CardFooter>
        <div class="inline-flex justify-center w-full gap-1">
          <Button v-if="gameStarted" variant="outline" @click="handleStop">
            <VueIcon icon="fa-solid:stop" size="15" />
            Stop
          </Button>
          <Button v-else variant="outline" @click="handleStart">
            <VueIcon icon="fa-solid:play" size="15" />
            Start
          </Button>

          <Button :disabled="!gameStarted" variant="destructive" @click="handleIncorrectAnswer">
            <VueIcon icon="fa-solid:exclamation" size="15" />
            Wrong answer
          </Button>
        </div>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useWebsocketUtilities } from '@/composables/utils'
import { wheelDetaults } from '@/data'
import { getBaseUrl } from '@/plugins/client'
import { useSongs } from '@/stores/songs'
import { useLocalStorage, useWebSocket } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'
import { toast } from 'vue-sonner'
import { RandomizerData } from '../randomizer'

import Spinner from '@/components/spinner/Spinner.vue'
import GenreRandomizer from '../randomizer/GenreRandomizer.vue'

import type { MatchedElement, Song, WebsocketBlindTestMessage } from '@/types'

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

    if (!gameStarted.value) {
      gameStarted.value = true
    }
  },
  onMessage() {
    const data = parseMessage<WebsocketBlindTestMessage>(ws.data.value)
    console.log(data)
    switch (data.action) {
      case 'connection_token':
        connectionToken.value = data.token

        if (data.team_one_id) {
          songsStore.cache.teams[0].id = data.team_one_id
        }

        if (data.team_two_id) {
          songsStore.cache.teams[1].id = data.team_two_id
        }
        break

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
        if (data.team_id) {
          if (data.points) {
            const team = songsStore.cache.teams.find(x => x.id === data.team_id)
            if (team) {
              team.score = data.points
            }
          }
        }
        break

      case 'song_skipped':
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
    toast.error('Warning', {
      description: 'Game has been disconnected',
      class: 'bg-yellow-100'
    })
  },
  onError() {
    toast.error('Error', {
      description: 'An error has occured'
    })
  }
})

/**
 * Function that gets called once the
 * spinning has finished
 *
 * @param value The genre to get
 */
function randomizerComplete(value: string | undefined | RandomizerData) {
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

/**
 *
 */
function handleFinalize() {
  songsStore.cache.currentStep += 1
}

/**
 * Returns the next song by excluding
 * those that were already played
 */
function handleIncorrectAnswer() {
  ws.send(sendMessage<WebsocketBlindTestMessage>({ action: 'skip_song' }))
  handleFinalize()
}

/**
 * Proxy function that can be used by parent elements
 * to trigger a websocket message on the team guess
 *
 * @param teamId The ID of the team
 * @param match The element that was matched
 */
function handleCorrectAnswer(teamId: string, match: MatchedElement) {
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

/**
 * Starts the game
 */
function handleStart() {
  ws.open()
}

/**
 * Stops the game
 */
function handleStop() {
  ws.close()
  toast.success('Stopped blind test')

  if (songsStore.cache) {
    songsStore.cache.songs = []
    songsStore.correctAnswers = []

    songsStore.cache.teams.forEach((x) => {
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
