<template>
  <section id="blindtest">
    <blindtest-layout>
      <template #video>
        <blindtest-video-block />
      </template>

      <template #default="attrs">
        <div id="players" :class="attrs.theme" class="h-full w-full p-5 overflow-hidden">
          <div class="flex items-start overflow-y-scroll gap-2 space-y-3 w-full">
            <blindtest-player-card v-for="(player, idx) in players" :id="`player-${idx}`" :key="idx" :player-id="player"  />
          </div>
        </div>
      </template>
    </blindtest-layout>

    <!-- Modals -->
    <blindtest-modals-active-game v-model:show="warnActiveGameModal" @proceed="() => stopGame(stopGameCallback)" />
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'blindtest'
})

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

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-30px);
  }
  60% {
    transform: translateY(-15px);
  }
}
</style>
