<template>
  <section id="blindtest" class="grid grid-cols-12 h-screen relative">
    <!-- Action Bar -->
    <action-bar />

    <!-- Video -->
    <div class="artist col-span-12 min-h-100 bg-primary-500 dark:bg-primary-900 p-20 relative">
      <div class="bg-linear-to-l from-primary-600 to-primary-900 absolute top-0 left-0 w-full h-full z-10 opacity-80 blur-5xl" />
      <div class="absolute top-0 left-0 w-full h-full flex justify-center items-center z-20 px-10 pt-[calc(2.5rem+50px)] pb-10">
        <slot name="video" />
      </div>
    </div>

    <slot>
      <!-- Teams -->
      <div class="col-span-6 bg-linear-to-r from-primary-100 via-primary-200 to-primary-300 p-5 overflow-hidden border-primary-100 border-10">
        <slot name="leftTeam" />
      </div>
  
      <div class="col-span-6 bg-linear-to-l from-primary-100 via-primary-200 to-primary-300 p-5 overflow-hidden border-primary-100 border-10">
        <slot name="rightTeam" />
      </div>
    </slot>

    <!-- Dock -->
    <action-dock />

    <!-- Modals -->
    <devices-modal v-model="showDevices" />
    <genre-randomizer ref="randomizerEl" v-model:show="showWheel" :items="wheelDefaults" @completed="randomizerComplete" />
  </section>
</template>

<script setup lang="ts">
import type { RandomizerData } from '@/components/blindtest/randomizer'

/**
 * Background artist image
 */
const songsStore = useSongs()
const { currentSong } = storeToRefs(songsStore)

const { css } = useStyleTag('.artist { background-image: url("default.jpg");')

watchDebounced(currentSong, (newSong) => {
  if (isDefined(newSong)) {
    css.value = `.artist { background-image: url("${newSong.artist.spotify_avatar}"); }`
  }
}, {
  debounce: 500
})

/**
 * Websocket
 */

const { isConnected, gameStarted, wsObject } = useGameWebsocket()

provide<boolean>('isConnected', isConnected.value)
provide<boolean>('gameStarted', gameStarted.value)

/**
 * Wheel Randomizer
 */

// const randomizeEl = useTemplateRef('randomizerEl')
const { showWheel, randomizerEl, randomizerComplete } = useWheelRandomizer(wsObject)

const wheelDefaults: RandomizerData[] = [
  { id: 1, value: 'Pop', bgColor: '#f87171', color: '#ffffff' },
  { id: 2, value: 'Rock', bgColor: '#60a5fa', color: '#ffffff' },
  { id: 3, value: 'Hip-Hop', bgColor: '#34d399', color: '#ffffff' },
  { id: 4, value: 'Jazz', bgColor: '#fbbf24', color: '#ffffff' },
  { id: 5, value: 'Classical', bgColor: '#a78bfa', color: '#ffffff' },
  { id: 6, value: 'Electronic', bgColor: '#f472b6', color: '#ffffff' },
  { id: 7, value: 'Metal', bgColor: '#9ca3af', color: '#ffffff' },
  { id: 8, value: 'Funk', bgColor: '#10b981', color: '#ffffff' },
  { id: 9, value: 'Reggae', bgColor: '#22d3ee', color: '#ffffff' }
]

/**
 * Modals
 */

const showDevices = ref(false)
</script>
