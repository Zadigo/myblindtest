<template>
  <transition mode="out-in" enter-from-class="animate-zoomout opacity-0" enter-active-class="" enter-to-class="animate-zoomin opacity-100" leave-from-class="animate-zoomin opacity-100" leave-active-class="" leave-to-class="animate-zoomout opacity-0">
    <volt-card v-if="player && isReady" class="self-center min-w-[300px]">
      <template #content>
        <div class="p-5 text-center">
          <h1 class="text-8xl font-bold text-primary-100">
            {{ player.points }}
          </h1>

          <p class="font-light text-primary-100">
            Points
          </p>


          <p class="mt-5 bg-primary-50 dark:bg-primary-800 text-primary-100 font-bold p-5 rounded-lg text-3xl">
            {{ player.name }}
          </p>

          <volt-contrast-button class="mt-5" @click="() => $emit('toggle-settings-modal')">
            <vue-icon icon="lucide:settings" />
          </volt-contrast-button>
        </div>
      </template>
    </volt-card>

    <base-game-loader v-else class="my-5" />

    <!-- <div class="animate-slidedown"></div> -->
  </transition>
</template>

<script setup lang="ts">
import type { BlindtestPlayer, Undefineable } from '@/types'

defineProps<{
  player: Undefineable<BlindtestPlayer>
  isReady: boolean
}>()

defineEmits<{ 'toggle-settings-modal': [] }>()
</script>
