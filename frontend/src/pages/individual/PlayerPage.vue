<template>
  <div class="relative h-screen w-full bg-no-repeat bg-center bg-cover" :style="{ backgroundImage: 'url(/default.jpg)'}">
    <volt-container size="sm">
      <div class="absolute top-4/12 left-1/2 transform -translate-x-1/2 z-50">
        {{ currentSettings }}

        <volt-card v-if="player" class="self-center">
          <template #content>
            <div class="p-5 text-center">
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

        <!-- <div class="rounded-xl bg-primary-700 dark:bg-primary-950 dark:text-primary-100 w-full space-y-2 h-200 flex justify-center items-center">
          <div class="p-10 md:px-20 overflow-hidden overflow-y-scroll space-y-3 w-full h-[calc(100vh-200px)]">
            <div v-for="idx in 10" :key="idx" class="p-5 bg-primary-100 dark:bg-primary-900 rounded-xl flex justify-around items-center space-x-5 w-full">
              <span class="font-bold text-5xl">{{ idx }}.</span>
              <h2 class="text-2xl mt-2">The Player's</h2>
              <div class="font-bold text-5xl text-primary-200 rounded-full p-4 bg-primary-500">56</div>
            </div>
          </div>
        </div> -->
      </div>

      <div class=" absolute top-0 left-0 h-screen w-full bg-linear-to-b from-primary-200 via-primary-300 to-primary-500 dark:from-primary-400 dark:via-primary-700 dark:to-primary-800 opacity-90 z-1" />
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
