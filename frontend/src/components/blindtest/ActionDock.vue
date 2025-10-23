<template>
  <div ref="dock" id="dock" class="col-span-12 bg-primary-100/30 border border-primary-100/80 h-auto min-w-100 w-150 absolute bottom-10 left-[calc(50%-calc(600px/2))] px-2 py-3 rounded-xl flex justify-center gap-2 z-40 overflow-hidden">
    <div v-for="item in filteredItems" :key="item.icon" :class="{ [`${animationClass }`]: item.animate }" class="p-1 bg-primary-50 rounded-lg w-13 h-13 flex justify-center items-center gap-2 cursor-pointer hover:bg-primary-100 transition hover:-translate-y-1" @click="item.action">
      <vue-icon :icon="item.icon" class="text-xl" />
    </div>

    <div class="p-1 bg-primary-50 rounded-lg ms-5 w-auto h-13 flex justify-center items-center gap-2 cursor-pointer hover:bg-primary-100 transition hover:-translate-y-1" @click="sendIncorrectAnswer">
      <vue-icon icon="lucide:x-square" class="text-xl" />
      Wrong answer
    </div>

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
    icon: 'lucide:stop',
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

const filteredItems = computed(() => {
  return items.filter((item) => {
    if (item.state === null) return true
    return item.state
  })
})
</script>
