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

    <!-- Teams -->
    <div class="col-span-6 bg-linear-to-r from-primary-100 via-primary-200 to-primary-300 p-5 overflow-hidden border-primary-100 border-10">
      <slot name="leftTeam" />
    </div>

    <div class="col-span-6 bg-linear-to-l from-primary-100 via-primary-200 to-primary-300 p-5 overflow-hidden border-primary-100 border-10">
      <slot name="rightTeam" />
    </div>

    <!-- Dock -->
    <action-dock />

    <!-- Modals -->
     <devices-modal v-model="showDevices" />
  </section>
</template>

<script setup lang="ts">
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

const { isConnected, gameStarted } = useGameWebsocket()

provide<boolean>('isConnected', isConnected.value)
provide<boolean>('gameStarted', gameStarted.value)

/**
 * Modals
 */

const showDevices = ref(false)
</script>
