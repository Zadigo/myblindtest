<template>
  <section id="blindtest">
    <blind-test-layout>
      <template #video>
        <video-block />
      </template>

      <template #default>
        <div id="players" class="col-span-12 bg-linear-to-r from-primary-100 via-primary-200 to-primary-300 p-5 overflow-hidden border-primary-100 border-10">
          <div class="grid grid-cols-10 overflow-y-scroll gap-2 space-y-3 w-full">
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
import { useGameWebsocketIndividual } from '@/composables'
import { ref } from 'vue'

/**
 * Websocket
 */

const { wsObject, players } = useGameWebsocketIndividual()
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
