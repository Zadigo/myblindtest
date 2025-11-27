<template>
  <section id="blindtest">
    <blind-test-layout>
      <template #video>
        <video-block />
      </template>

      <template #default="attrs">
        <div id="players" :class="attrs.theme" class="h-full w-full p-5 overflow-hidden">
          <div class="flex items-start overflow-y-scroll gap-2 space-y-3 w-full">
            <player-card v-for="(player, idx) in players" :key="idx" :player-id="player"  />
          </div>
        </div>
      </template>
    </blind-test-layout>

    <!-- Modals -->
    <active-game v-model="warnActiveGameModal" @proceed="() => stopGame(stopGameCallback)" />
  </section>
</template>

<script setup lang="ts">
import { useAdminWebsocket } from '@/composables'

/**
 * Websocket
 */

const { wsObject, players } = useAdminWebsocket()
wsObject.open()

const warnActiveGameModal = ref(false)

function stopGame(callback: () => void) {
  // Implementation for stopping the game
  callback()
}

function stopGameCallback() {
  // Callback logic after stopping the game
}

/**
 * SEO
 */

useHead({
  title: 'Blindtest',
  meta: [
    {
      name: 'description',
      content: 'Play an exciting blindtest game with your friends! Guess the songs and compete for the highest score.'
    }
  ]
})
</script>

<style scoped>
#players>div::-webkit-scrollbar {
  display: none;
}
</style>
