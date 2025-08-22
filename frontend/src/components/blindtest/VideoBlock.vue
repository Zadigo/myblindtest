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
          {{ currentStep }}/-
        </p>

        <div id="video-wrapper" class="rounded-md overflow-hidden flex justify-center items-center max-w-full">
          <iframe v-if="gameStarted && currentSong" :src="currentSong.youtube" :title="currentSong.artist.name" class="max-w-full h-auto block" width="400" height="200" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" />
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
          <volt-button v-if="gameStarted" @click="() => handleStop()">
            <vue-icon icon="fa-solid:stop" size="15" />
            Stop
          </volt-button>
          <volt-button v-else variant="outlined" @click="() => handleStart()">
            <vue-icon icon="fa-solid:play" size="15" />
            Start
          </volt-button>

          <volt-button :disabled="!gameStarted" variant="destructive" @click="() => sendIncorrectAnswer()">
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
import { toast } from 'vue-sonner'

import type { MatchedPart } from '@/data'
import type { DefaultActions, VideoBlockExposedMethods, WebsocketSendGuess } from '@/types'

const sessionStore = useSessionStore()
const { currentSettings } = storeToRefs(sessionStore)

const songsStore = useSongs()

const { gameStarted, currentSong, currentStep, correctAnswers } = storeToRefs(songsStore)
const { wsObject } = useGameWebsocket()

const { send, parse } = useWebsocketMessage()

/**
 * Callback function used after a correct or
 * incorrect answer was triggered
 */
function handleFinalize() {
  songsStore.incrementStep()
}

/**
 * Returns the next song by excluding
 * those that were already played
 */
function sendIncorrectAnswer() {
  const result = send<{ action: DefaultActions }>({ action: 'skip_song' })

  if (result) {
    wsObject.send(result)
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
function sendCorrectAnswer(teamId: string, match: MatchedPart) {
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
    wsObject.send(result)
    handleFinalize()
  }
}

/**
 * Starts the game
 */
function handleStart() {
  wsObject.open()
}

const teamStore = useTeamsStore()
const { teamOne, teamTwo } = storeToRefs(teamStore)

/**
 * Stops the game
 */
function handleStop() {
  toast.success('Stopped blind test')
  
  correctAnswers.value = []
  
  teamOne.value.score = 0
  teamTwo.value.score = 0

  songsStore.resetStep()

  wsObject.close()
}

const { showWheel, randomizerEl, randomizerComplete } = useWheelRandomizer(wsObject.ws)

defineExpose<VideoBlockExposedMethods>({
  sendCorrectAnswer,
  sendIncorrectAnswer
})
</script>
