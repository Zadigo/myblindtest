<template>
  <div ref="dockEl" id="dock" class="col-span-12 bg-primary-100/30 dark:bg-primary-950 dark:border-none dark:shadow-2xl border border-primary-100/80 h-auto min-w-100 w-150 absolute bottom-10 left-[calc(50%-calc(600px/2))] px-2 py-3 rounded-xl flex justify-center gap-2 z-40 overflow-hidden">
    <transition-group enter-from-class="animate-fadeinup" enter-to-class="animate-fadeindown" leave-from-class="animate-fadeindown" leave-to-class="animate-fadeinup">
      <volt-button v-for="item in items" :key="item.icon" @click="item.action">
        <vue-icon :icon="item.icon" class="text-xl" />
      </volt-button>
    </transition-group>

    <sound-effect id="sound-wrong-answer" name="cinematic-hit">
      <template #default="{ attrs }">
        <volt-secondary-button @click="attrs.playSound(sendIncorrectAnswer)">
          <vue-icon icon="lucide:x-square" class="text-xl" />
          Wrong answer
        </volt-secondary-button>
      </template>
    </sound-effect>

    {{ gameStarted }}
  </div>
</template>

<script setup lang="ts">
import { useToast } from 'primevue/usetoast'

const toast = useToast()

/**
 * Ranadomizer
 */

const { showWheel } = useWheelRandomizer()

/**
 * Websocket
 */

const { wsObject, gameStarted } = useGameWebsocketIndividual()
const { startGame, stopGame, sendIncorrectAnswer } = useGameActions(wsObject, gameStarted)

const songsStore = useSongs()
const { correctAnswers } = storeToRefs(songsStore)

// Callback function executed after stopping the game
// to reset scores and correct answers
function stopGameCallback() {
  correctAnswers.value = []

  songsStore.songsPlayed = []
  songsStore.resetStep()
  toast.add({ severity: 'info', summary: 'Game Stopped', detail: 'The game has been successfully stopped and reset.', life: 8000 })
}

/**
 * Timer
 */

const { restart, hasTimer } = useGameCountdown()

/**
 * Dock Buttons
 */

const items = computed(() => {
  const baseItems = [
    {
      name: 'Play',
      icon: 'lucide:play',
      action: startGame
    },
    {
      name: 'Stop',
      icon: 'lucide:circle-stop',
      action: () => stopGame(stopGameCallback)
    },
    {
      name: 'Randomizer',
      icon: 'lucide:zap',
      action: () => { showWheel.value = !showWheel.value }
    }
  ]

  if (hasTimer.value) {
    baseItems.splice(1, 0, {
      name: 'Restart Timer',
      icon: 'lucide:timer-reset',
      action: restart
    })
  }

  return baseItems
})
</script>
