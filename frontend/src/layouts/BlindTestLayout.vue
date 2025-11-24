<template>
  <section id="blindtest" class="relative h-screen w-full bg-primary-200 dark:bg-primary-800">
    <!-- Action Bar -->
    <action-bar />

    <!-- Main Content -->
    <div class="grid grid-cols-12 grid-rows-12 w-full h-full">
      <div class="relative col-span-12 row-span-8 overflow-hidden">
        <!-- Overlay -->
        <div class="absolute filter brightness-50 top-0 left-0 z-40 w-full h-full opacity-90 bg-linear-to-t dark:from-primary-950 dark:via-primary-700 dark:to-primary-600" />

        <!-- Background -->
        <div id="artist" class="absolute top-0 left-0 w-full h-full bg-no-repeat bg-cover bg-center blur-sm z-20 bg-fixed" :style="{ backgroundImage: `url(${currentSong?.artist.spotify_avatar || '/dancing1.jpg'})` }" />

        <!-- Video -->
        <!-- border-8 border-primary-100 dark:border-primary-800 -->
        <div class="absolute z-50 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-xl overflow-hidden shadow-2xl w-5xl">
          <slot name="video" />
        </div>
      </div>

      <!-- Bottom -->
      <div class="col-span-12 row-span-4">
        <slot :theme="childTheme" />
      </div>
    </div>

    <!-- Dock -->
    <action-dock />

    <!-- Modals -->
    <devices-modal v-model="showDevices" />
    <connection-url v-model:show="showConnectionUrl" />
    <genre-randomizer ref="randomizerEl" v-model:show="showWheel" :items="wheelDefaults" @completed="randomizerComplete" />
  </section>
</template>

<script setup lang="ts">
import { wheelDefaults } from '@/composables'

/**
 * Background artist image
 */
const songsStore = useSongs()
const { currentSong } = storeToRefs(songsStore)

/**
 * Websocket
 */

const { isConnected, gameStarted, wsObject } = useGameWebsocketIndividual()

provide<boolean>('isConnected', isConnected.value)
provide<boolean>('gameStarted', gameStarted.value)

/**
 * Wheel Randomizer
 */

// const randomizeEl = useTemplateRef('randomizerEl')
const { showWheel, randomizerEl, randomizerComplete } = useWheelRandomizer(wsObject)

/**
 * Modals
 */

const showDevices = ref(false)
const showConnectionUrl = ref(false)

/**
 * Theme
 */

const childTheme = ref([
  'border-10',
  'bg-linear-to-r from-primary-100 via-primary-200 to-primary-300',
  'dark:bg-linear-to-t dark:from-primary-500 dark:via-primary-700 dark:to-primary-900',
  'border-primary-100 dark:border-primary-800',
])
</script>

<style scoped>
#artist {
  transition: background-image 0.5s cubic-bezier(.74, .08, .32, .85);
  animation: fadeIn 10s cubic-bezier(.74, .08, .32, .85) infinite;
}

@keyframes fadeIn {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  75% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}
</style>
