<template>
  <div class="h-screen w-full bg-linear-to-b from-primary-200 via-primary-300 to-primary-500 flex items-center justify-center">
    <volt-container size="sm">
      {{ currentSettings?.players }}
      <volt-card v-if="player">
        <template #content>
          <div  class="p-5 text-center">
            <h1 class="text-8xl font-bold text-primary-100">
              {{ player.points }}
            </h1>

            <p class="font-light text-primary-100">
              Points
            </p>


            <p class="mt-5 bg-primary-50 dark:bg-primary-800 p-5 rounded-lg text-lg">
              {{ player.name }}
            </p>
          </div>
        </template>
      </volt-card>

      <base-game-loader v-else class="my-5" />    
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
 * Ranking
 */

const { currentSettings } = useSession()

 onMounted(() => {
   console.log(currentSettings.value)
 })
</script>
