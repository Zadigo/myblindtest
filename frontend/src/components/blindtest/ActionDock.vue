<template>
  <div ref="dock" id="dock" class="col-span-12 bg-primary-100/30 border border-primary-100/80 h-auto min-w-100 w-150 absolute bottom-10 left-[calc(50%-calc(600px/2))] px-2 py-3 rounded-xl flex justify-center gap-2 z-40 overflow-hidden">
    <volt-button v-for="item in items" :key="item.icon" :class="{ [`${animationClass}`]: item.animate }" @click="item.action">
      <vue-icon :icon="item.icon" class="text-xl" />
    </volt-button>

    <volt-secondary-button @click="sendIncorrectAnswer">
      <vue-icon icon="lucide:x-square" class="text-xl" />
      Wrong answer
    </volt-secondary-button>

    {{ gameStarted }}
  </div>
</template>

<script setup lang="ts">
import { useToast } from 'primevue/usetoast'

const toast = useToast()

/**
 * Websocket
 */

// 'animate-bounce animate-ease-in-out animate-duration-1000'
const animationClass = ''
const { startGame, stopGame, gameStarted, sendIncorrectAnswer } = useGameWebsocket()

const songsStore = useSongs()
const { correctAnswers } = storeToRefs(songsStore)

const teamStore = useTeamsStore()
const { teamOne, teamTwo } = storeToRefs(teamStore)


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

  songsStore.songsPlayed = []
  songsStore.resetStep()
  toast.add({ severity: 'info', summary: 'Game Stopped', detail: 'The game has been successfully stopped and reset.', life: 8000 })
}

const items = [
  { 
    icon: 'lucide:play',
    state: !gameStarted.value,
    animate: !gameStarted.value,
    action: startGame
  },
  { 
    icon: 'lucide:circle-stop',
    state: gameStarted.value,
    animate: false,
    action: () => stopGame(stopGameCallback)
  },
  { 
    icon: 'lucide:zap',
    state: null,
    animate: false,
    action: () => console.log('Stop')
  }
]
</script>
