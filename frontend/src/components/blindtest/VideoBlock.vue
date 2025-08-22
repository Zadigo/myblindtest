<template>
  <div class="absolute my-10 left-2/6 w-4/12 bg-secondary">
    <volt-card class="border-none shadow-md">
      <template #content>
        <div class="flex justify-between items-center">
          <div v-if="currentSong">
            <p class="font-bold">
              {{ currentSong.name }} <span class="font-semibold">({{ currentSong.artist.name }})</span>
            </p>

            <div class="inline-flex gap-1 my-2">
              <template v-for="i in 5" :key="i">
                <vue-icon v-if="i <= currentSong.difficulty" icon="fa-solid:star" />
                <vue-icon v-else icon="fa-solid:star" class="text-slate-50" />
              </template>
            </div>

            <div>
              <volt-badge variant="default">
                {{ currentSong.genre }}
              </volt-badge>
            </div>
          </div>

          <div class="flex justify-end gap-2">
            <volt-button variant="outline">
              <router-link :to="{ name: 'home' }">
                <vue-icon icon="fa-solid:home" size="15" />
              </router-link>
            </volt-button>

            <volt-button variant="outline" @click="showWheel=!showWheel">
              <vue-icon icon="fa-solid:bolt" size="15" />
            </volt-button>
          </div>
        </div>

        <!-- Video -->
        <p class="font-bold mb-3">
          {{ songsStore.cache.currentStep }}/-
        </p>

        <div id="video-wrapper" class="rounded-md overflow-hidden flex justify-center items-center max-w-full">
          <iframe v-if="gameStarted && currentSong" :src="songsStore.currentSong.youtube" :title="songsStore.currentSong.artist.name" class="max-w-full h-auto block" width="400" height="200" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" />
          <Spinner v-else name="loader-12" />
        </div>

        <!-- Wheel -->
        <Transition mode="out-in" name="animate__animated" enter-active-class="animate__animated animate__fadeInDown" leave-active-class="animate__animated animate__fadeOutDown">
          <div v-if="showWheel">
            <genre-randomizer ref="randomizerEl" :items="wheelDetaults" @completed="randomizerComplete" />
          </div>
        </Transition>
      </template>

      <template #footer>
        <div class="inline-flex justify-center w-full gap-1">
          <volt-button v-if="gameStarted" @click="handleStop">
            <vue-icon icon="fa-solid:stop" size="15" />
            Stop
          </volt-button>
          <volt-button v-else variant="outlined" @click="handleStart">
            <vue-icon icon="fa-solid:play" size="15" />
            Start
          </volt-button>

          <volt-button :disabled="!gameStarted" variant="destructive" @click="handleIncorrectAnswer">
            <vue-icon icon="fa-solid:exclamation" size="15" />
            Wrong answer
          </volt-button>
        </div>
      </template>
    </volt-card>
  </div>
</template>

<script setup lang="ts">
import { useSessionStore } from '@/stores/session'
import { useWebsocketMessage } from '@/utils'
import { toast } from 'vue-sonner'

import type { MatchedPart } from '@/data'
import type { DefaultActions, Song, VideoBlockExposedMethods, WebsocketBlindTestMessage, WebsocketRandomizeGenre, WebsocketSendGuess, WebsocketSettings } from '@/types'
import type { RandomizerData } from '../randomizer'

const sessionStore = useSessionStore()
const songsStore = useSongs()
const { gameStarted, currentSong } = storeToRefs(songsStore)
const { send, parse } = useWebsocketMessage()

const connectionToken = useLocalStorage<string | null | undefined>('connectionToken', null)

const showWheel = ref<boolean>(false)
const randomizerEl = ref<HTMLElement>()

const ws = useWebSocket('ws://127.0.0.1:8000/ws/songs', {
  immediate: false,
  onConnected(ws) {
    const settings = songsStore.cache.settings

    const result = send<WebsocketSettings>({
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
    })

    if (result) {
      ws.send(result)

      toast.success('Info', {
        description: 'Started blind test'
      })

      if (!gameStarted.value) {
        gameStarted.value = true
      }
    }
  },
  onMessage(_ws, event: MessageEvent<string>) {
    const data = parse<WebsocketBlindTestMessage>(event.data)

    console.log(data)

    if (data) {
      switch (data.action) {
        case 'connection_token': {
          connectionToken.value = data.token

          if (data.team_one_id) {
            songsStore.cache.teams[0].id = data.team_one_id
          }

          if (data.team_two_id) {
            songsStore.cache.teams[1].id = data.team_two_id
          }
          break
        }

        case 'game_started': {
          gameStarted.value = true
          break
        }

        case 'song_new': {
          songsStore.cache.songs.push(data.song as Song)
          break
        }

        case 'timer_tick': {
          break
        }

        case 'guess_correct': {
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
        }

        case 'song_skipped': {
          break
        }

        case 'randomize_genre': {
          songsStore.cache.songs.push(data.song as Song)
          break
        }

        case 'device_connected': {
          const message = send<WebsocketBlindTestMessage>({
            action: 'update_device_cache',
            cache: songsStore.cache
          })

          if (message) {
            ws.send(message)

            toast.success('Device', {
              description: 'Projecton device connected'
            })
          }
          break
        }

        case 'device_disconnected': {
          toast.success('Device', {
            description: 'Projecton device disconnected'
          })
          break
        }

        case 'error': {
          toast.error('Error', {
            description: data.error
          })
          break
        }

        default: {
          break
        }
      }
    }
  },
  onDisconnected() {
    gameStarted.value = false
    toast.error('Warning', {
      description: 'Game has been disconnected',
      unstyled: true,
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

      const result = send<WebsocketRandomizeGenre>({
        action: 'randomize_genre',
        temporary_genre: value
      })

      if (result) {
        ws.send(result)
      }
    }, 3000)
  }
}

/**
 * Callback function used after a correct or
 * incorrect answer was triggered
 */
function handleFinalize() {
  songsStore.cache.currentStep += 1
}

/**
 * Returns the next song by excluding
 * those that were already played
 */
function handleIncorrectAnswer() {
  const result = send<{ action: DefaultActions }>({ action: 'skip_song' })

  if (result) {
    ws.send(result)
    handleFinalize()
  }
}

/**
 * Proxy function that can be used by parent elements
 * to trigger a websocket message on the team guess
 *
 * @param teamId The ID of the team
 * @param match The element that was matched
 */
function handleCorrectAnswer(teamId: string, match: MatchedPart) {
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

  const result = send<WebsocketSendGuess>({
    action: 'submit_guess',
    team_id: teamId,
    title_match,
    artist_match
  })

  console.log('handleCorrectAnswer', result)

  if (result) {
    ws.send(result)
    handleFinalize()
  }
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

defineExpose<VideoBlockExposedMethods>({
  handleCorrectAnswer,
  handleIncorrectAnswer
})
</script>
