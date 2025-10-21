<template>
  <div class="absolute my-10 left-2/6 w-4/12 bg-secondary space-y-2">
    <!-- Code. State -->
    <volt-card>
      <template #content>
        Connected: {{ isConnected }}
        Game started: {{ gameStarted }}
        <div class="flex justify-between items-center">
          <volt-badge v-if="isConnected" class="animate-pulse animation-duration-5000">Connected</volt-badge>
          <volt-badge v-else class="cursor-pointer" @click="wsObject.open()">Disconnected</volt-badge>

          <div class="py-2 px-5 rounded-md bg-primary-100 flex justify-start items-center gap-5 cursor-pointer ease-in-out hover:bg-primary-200" @click="() => copy()">
            <p class="text-primary-600">{{ sessionId }}</p>

            <div class="p-1 bg-primary-50 dark:bg-primary-500 rounded-lg">
              <vue-icon icon="fa-solid:copy" class="dark:text-surface-50" />
            </div>
          </div>
        </div>
      </template>
    </volt-card>

    <!-- Video Panel -->
    <volt-card class="border-none shadow-md">
      <template #content>
        <!-- Song Info -->
        <video-block-song-info :currentSong="currentSong" @show:wheel="showWheel = !showWheel" />

        <p class="font-bold py-3">
          {{ currentStep }}/-
        </p>
        
        <!-- Video -->
        <div id="video-wrapper" class="rounded-md overflow-hidden flex justify-center items-center max-w-full">
          <iframe v-if="gameStarted && currentSong" :src="currentSong.youtube" :title="currentSong.artist.name" class="max-w-full h-auto block" width="400" height="200" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" />
          <div v-else class="py-15">
            <Spinner name="loader-12" />
          </div>
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
          <volt-secondary-button v-if="gameStarted" @click="() => stopGame(stopGameCallback)">
            <vue-icon icon="fa-solid:stop" size="15" />
            Stop {{ gameStarted }}
          </volt-secondary-button>
          <volt-button v-else variant="outlined" @click="() => startGame()">
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
import { useToast } from 'primevue/usetoast'

const toast = useToast()

/**
 * Websocket
 */

const { wsObject, startGame, stopGame, isConnected, sendIncorrectAnswer, gameStarted } = useGameWebsocket()

const songsStore = useSongs()
const { currentSong, currentStep, correctAnswers } = storeToRefs(songsStore)

const teamStore = useTeamsStore()
const { teamOne, teamTwo } = storeToRefs(teamStore)

/**
 * Actions
 */

 // Callback function executed after stopping the game
 // to reset scores and correct answers
function stopGameCallback() {
  correctAnswers.value = []
  
  if (teamOne.value) {
    teamOne.value.score = 0
  }
  
  if (teamTwo.value) {
    teamTwo.value.score = 0
  }

  songsStore.resetStep()
  toast.add({ severity: 'info', summary: 'Game Stopped', detail: 'The game has been successfully stopped and reset.', life: 8000 })
}

/**
 * Wheel Randomizer
 */

const { showWheel, randomizerEl, randomizerComplete } = useWheelRandomizer(wsObject.ws)

/**
 * Session copy
 */

const { sessionId } = useGlobalSessionState()
const { copy } = useClipboard({ source: sessionId })
</script>
