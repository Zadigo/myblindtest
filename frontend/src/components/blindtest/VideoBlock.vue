<template>
  <transition mode="in-out">
    <div id="video" v-if="gameStarted" class="h-full flex justify-center gap-5 p-5">
      <div v-if="currentSong" class="flex justify-left overflow-hidden rounded-xl min-height-[200px]">
        <iframe :src="currentSong.youtube" class="max-w-full h-auto block" width="400" height="200" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" />
      </div>

      <div v-if="currentSong" class="mt-10 space-y-2">
        <h1 class="text-6xl text-surface-50 font-bold opacity-50">
          {{ currentSong.name }}
        </h1>
        <h1 class="text-4xl text-surface-50 font-bold">
          {{ currentSong.artist.name }}
        </h1>

        <!-- Infos -->
        <div class="flex items-center gap-2 mt-5">
          <!-- Genre -->
          <volt-badge variant="default">
            {{ currentSong.genre }}
          </volt-badge>

          <!-- Difficulty -->
          <volt-badge severity="info">
            <vue-icon v-for="i in currentSong.difficulty" :key="i" icon="lucide:star" />
          </volt-badge>
        </div>

        <!-- Other -->
        <div class="flex gap-2">
          <div class="p-2 bg-primary-100 rounded-lg text-2xl mt-5 opacity-80 w-30 text-center">
            {{ currentStep }} of <span class="font-semibold">40</span>
          </div>
          <div class="p-2 bg-primary-100 rounded-lg text-2xl mt-5 opacity-80 w-30 text-center" @click="start()">
            {{ toMinutes }}
          </div>
        </div>
      </div>
    </div>

    <div v-else class="py-15">
      {{ gameStarted }}
      <spinner name="loader-12" />
    </div>
  </transition>
</template>

<script setup lang="ts">
import { useSound } from '@vueuse/sound'

const { gameStarted } = useGameWebsocketIndividual()

/**
 * Song
 */

const songsStore = useSongs()
const { currentSong, currentStep } = storeToRefs(songsStore)

const { play } = useSound('/battery.mp3', { playbackRate: 1.5 })

watch(currentSong, () => {
  if (currentStep.value > 1) {
    play()
  }
})

/**
 * Settings
 */

const { currentSettings } = useSession()

/**
 * Countdown
 */

const { start, pause, reset, toMinutes } = useGameCountdown(currentSettings.value?.settings.timeLimit)

onBeforeUnmount(() => {
  pause()
  reset()
})
</script>
