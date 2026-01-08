<template>
  <div id="video" class="h-full flex justify-start gap-8 p-5 z-20">
    <div class="bg-primary-300/30 dark:bg-primary-900 flex justify-left items-center overflow-hidden rounded-xl w-[400px] h-[300px] min-height-[200px]">
      <!-- frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" -->
      <iframe v-if="gameStarted && currentSong" id="player" :src="currentSong.youtube" class="max-w-full h-auto block" width="400" height="200" />
      <volt-loaders-bars-loader v-else />
    </div>

    <div v-if="gameStarted && currentSong" class="mt-10 space-y-2">
      <h1 class="text-6xl text-surface-50 font-bold opacity-50">
        {{ currentSong.name }}
      </h1>

      <h3 class="text-4xl text-surface-50 opacity-80 font-bold">
        {{ currentSong.artist.name }}
      </h3>

      <!-- Infos -->
      <div class="flex items-center gap-2 mt-5">
        <!-- Genre -->
        <volt-badge severity="contrast">
          {{ currentSong.genre }}
        </volt-badge>

        <!-- Difficulty -->
        <volt-badge severity="contrast">
          <icon v-for="i in currentSong.difficulty" :key="i" name="lucide:star" />
        </volt-badge>
      </div>

      <div class="flex gap-2">
        <!-- Current Step -->
        <div class="p-2 bg-secondary-500/70 text-secondary-100 rounded-lg text-2xl mt-5 opacity-80 w-30 text-center">
          <template v-if="currentSettings">
            <div v-if="currentSettings.settings.rounds > 0">{{ currentStep }} of <span class="font-semibold">40</span></div>
            <div v-else>{{ currentSettings.settings.rounds }}</div>
          </template>

          <div v-else>
            <volt-skeleton height="20px" width="50px" />
          </div>
        </div>

        <!-- Timer -->
        <div id="game-timer" ref="timeEl" class="p-2 bg-secondary-500/70 text-secondary-100 rounded-lg text-2xl mt-5 opacity-80 w-30 text-center">
          {{ timerToMinutes }}
        </div>
      </div>
    </div>

    <div v-else class="flex-col content-center">
      <div class="space-y-2">
        <volt-skeleton height="30px" width="300px" />
        <volt-skeleton height="30px" width="150px" />
        <volt-skeleton height="30px" width="170px" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSound } from '@vueuse/sound'

const { gameStarted } = useAdminWebsocket()

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

const { lessThanFiveSeconds, lessThanTenSeconds, timerToMinutes } = useGameCountdown()
const timerEl = useTemplateRef<HTMLElement>('timerEl')

watch(lessThanTenSeconds, (state) => {
  if (state) {
    timerEl.value?.classList.add('less-than-ten-seconds')
  } else {
    timerEl.value?.classList.remove('less-than-ten-seconds')
  }
})

watch(lessThanFiveSeconds, (state) => {
  console.log(state)
  if (state) {
    timerEl.value?.classList.add('less-than-five-seconds')
  } else {
    timerEl.value?.classList.remove('less-than-five-seconds')
  }
})
</script>

<style scoped>
#game-timer.less-than-ten-seconds {
  animation: timer-pulse 1s infinite;
}

#game-timer.less-than-five-seconds {
  animation: timer-pulse 0.5s infinite;
}

@keyframes timer-pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
  }
}
</style>
