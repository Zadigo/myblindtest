<template>
  <div class="relative">
    <!-- State -->
    <div :class="cardTheme" class="w-[500px] rounded-xl px-5 pt-5 pb-10 text-center absolute top-0 left-1/2 transform -translate-x-1/2">
      <h1 :class="themeTitle" class="text-6xl font-bold uppercase">
        {{ textDisplay }}
      </h1>
    </div>

    <!-- Image -->
    <div class="absolute top-35 left-1/2 transform -translate-x-1/2 w-200 h-200">
      <!-- <img v-if="isReady" :src="correctSong?.artist.spotify_avatar" :class="imageTheme" :alt="correctSong?.artist.name">
      <img v-else src="/default.jpg" :class="imageTheme" alt=""> -->
      <img v-if="correctSong" :src="correctSong.artist.spotify_avatar" :alt="correctSong.artist.name" :class="imageTheme" />
    </div>

    <!-- Answer -->
    <div class="absolute top-80 w-[500px] left-1/2 transform -translate-x-1/2 text-center">
      <h1 :class="textTheme" class="text-7xl font-bold">
        {{ correctSong?.name }}
      </h1>

      <h2 :class="textTheme" class="text-3xl">
        {{ correctSong?.artist.name }}
      </h2>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Nullable, Song } from '@/types'

const props = defineProps<{ 
  correctSong: Nullable<Song>
  isCorrectGuess: boolean
  isIncorrectGuess: boolean
  }>()

/**
 * Artist image
 */

const { isLoading, state, isReady } = useImage({ src: props.correctSong?.artist.spotify_avatar || '', alt: 'Artist Image' })

console.log(isLoading.value, state.value, isReady.value)

/**
 * Themes
 */

const imageTheme = computed(() => {
  return [
    'aspect-square w-40 h-40 object-cover rounded-full mx-auto shadow-xl border-10',
    {
      'border-secondary-100 dark:border-secondary-800': props.isCorrectGuess,
      'border-primary-100 dark:border-primary-800': props.isIncorrectGuess,
      'border-neutral-200 dark:border-neutral-900': !props.isCorrectGuess && !props.isIncorrectGuess
    }
  ]
})

const cardTheme = computed(() => {
  return {
    'bg-secondary-100 dark:bg-secondary-800': props.isCorrectGuess,
    'bg-primary-100 dark:bg-primary-800': props.isIncorrectGuess,
    'bg-neutral-50 dark:bg-neutral-900': !props.isCorrectGuess && !props.isIncorrectGuess,
  }
})

const textTheme = computed(() => {
  return {
    'text-secondary-300': props.isCorrectGuess,
    'text-primary-200': props.isIncorrectGuess,
    'text-neutral-600': !props.isCorrectGuess && !props.isIncorrectGuess
  }
})

const themeTitle = computed(() => {
  return {
    'text-secondary-500/80': props.isCorrectGuess,
    'text-primary-100/30': props.isIncorrectGuess,
    'text-neutral-100/40': !props.isCorrectGuess && !props.isIncorrectGuess
  }
})

const textDisplay = computed(() => {
  return props.isCorrectGuess ? 'Good answer!' : props.isIncorrectGuess ? 'Wrong Answer!' : 'No answers given'
})
</script>
