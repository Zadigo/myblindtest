<template>
  <div class="h-screen w-full bg-linear-to-b from-primary-100 via-primary-200 to-primary-300 flex items-center justify-center">
    <volt-container size="sm">
      <!-- <base-game-loader class="my-5" /> -->
    
      <volt-card>
        <template #content>
          <div v-if="player" class="p-5 text-center">
            <h1 class="text-8xl font-bold">
              {{ player.points }}
            </h1>

            <p class="font-light">
              Points
            </p>

            <p class="mt-5 bg-primary-50 p-5 rounded-lg text-lg">
              {{ player.name }}
            </p>
          </div>
        </template>
      </volt-card>
    </volt-container>
  </div>
</template>

<script setup lang="ts">
/**
 * Websocket
 */

const { wsObject, player } = useGameWebsocketIndividualPlayer()
wsObject.open()

/**
 * Player
 */
</script>
