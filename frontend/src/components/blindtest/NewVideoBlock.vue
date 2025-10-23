<template>
  <transition mode="in-out">
    <div id="video" v-if="gameStarted" class="h-full flex justify-center gap-10">
      <div v-if="currentSong" class="flex justify-left">
        <volt-card class="h-full">
          <template #content>
            <iframe :src="currentSong.youtube" class="max-w-full h-auto block" width="400" height="200" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" />
          </template>
        </volt-card>
      </div>

      <div v-if="currentSong" class="mt-10 space-y-2">
        <h1 class="text-6xl text-surface-50 font-bold">
          {{ currentSong.artist.name }} - <span class="opacity-50">{{ currentSong.name }}</span>
        </h1>

        <!-- Infos -->
        <div class="flex items-center gap-2">
          <!-- Genre -->
          <volt-badge variant="default">
            {{ currentSong.genre }}
          </volt-badge>

          <!-- Difficulty -->
          <volt-badge severity="info">
            <vue-icon v-for="i in currentSong.difficulty" :key="i" icon="lucide:star" />
          </volt-badge>
        </div>

        <!-- Other -->
        <div class="flex gap-2">
          <div class="p-2 bg-primary-100 rounded-lg text-2xl mt-15 opacity-80 w-30 text-center">
            {{ currentStep }} of <span class="font-semibold">40</span>
          </div>
          <div class="p-2 bg-primary-100 rounded-lg text-2xl mt-15 opacity-80 w-30 text-center">
            11:00
          </div>
        </div>
      </div>
    </div>

    <div v-else class="py-15">
      {{ gameStarted }}
      <spinner name="loader-12" />
    </div>
  </transition>
</template>

<script setup lang="ts">
const { gameStarted } = useGameWebsocket()

/**
 * Song
 */

const songsStore = useSongs()
const { currentSong, currentStep } = storeToRefs(songsStore)

/**
 * Settings
 */

const { currentSettings } = useGlobalSessionState()
</script>
