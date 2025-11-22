<template>
  <section id="blindtest">
    <players-layout>
      <template #video>
        <video-block />
      </template>

      <template #default>
        <div id="players" class="col-span-12 bg-linear-to-r from-primary-100 via-primary-200 to-primary-300 p-5 overflow-hidden border-primary-100 border-10">
          <div class="grid grid-cols-10 overflow-y-scroll gap-2 space-y-3 w-full">
            <volt-card v-for="(player, idx) in players" :key="idx">
              <template #content>
                <div class="text-center">
                  <div class="h-20 w-20 overflow-hidden rounded-full mb-2">
                    <img src="/profile.png" class="aspect-square object-cover" alt="Player Profile">
                  </div>

                  <h5 class="font-bold mb-4">
                    {{ player }}
                  </h5>

                  <div class="space-x-2">
                    <volt-button>
                      <vue-icon name="i-lucide:x" />
                    </volt-button>
                    <volt-button>
                      <vue-icon name="i-lucide:check" />
                    </volt-button>
                  </div>
                </div>
              </template>
            </volt-card>
          </div>
        </div>
      </template>
    </players-layout>

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
  title: 'Individual Blindtest',
  meta: [
    {
      name: 'description',
      content: 'Play an exciting blindtest game with your friends! Guess the songs and compete for the highest score.'
    }
  ]
})
</script>
