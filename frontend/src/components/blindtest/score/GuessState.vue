<template>
  <div class="relative">
    <div :class="cardTheme" class="w-[500px] rounded-xl px-5 pt-5 pb-10 text-center absolute top-0 left-1/2 transform -translate-x-1/2">
      <h1 :class="themeTitle" class="text-6xl font-bold uppercase">
        Good Answer!
      </h1>
    </div>

    <div class="absolute top-35 left-1/2 transform -translate-x-1/2 w-200 h-200">
      <img v-if="isReady" :src="correctSong?.artist.spotify_avatar" :class="imageTheme" :alt="correctSong?.artist.name">
      <img v-else src="/default.jpg" :class="imageTheme" alt="">
    </div>

    <div class="absolute top-80 w-[500px] left-1/2 transform -translate-x-1/2 text-center">
      <h1 :class="textTheme" class="text-7xl font-bold">
        Artist song
      </h1>
  
      <h2 :class="textTheme" class="text-3xl">
        Artist name
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
 * Card animation
 */

const keyframes = ref([
  { transform: 'rotate(0deg)' },
  { transform: 'rotate(10deg) scale(1.10)' },
  { transform: 'rotate(-10deg) scale(1)' },
  { transform: 'rotate(0deg)' },
  { transform: 'rotate(20deg) scale(0.95)' },
  { transform: 'rotate(-10deg) scale(1)' },
  { transform: 'rotate(0deg)' }
])

const cardEl = useTemplateRef<HTMLDivElement>('cardEl')
useAnimate(cardEl, keyframes, 1000)

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
      'border-primary-200 dark:border-primary-800': !props.isCorrectGuess && !props.isIncorrectGuess
    }
  ]
})

const cardTheme = computed(() => {
  return {
    'bg-secondary-100 dark:bg-secondary-800': props.isCorrectGuess,
    'bg-primary-100 dark:bg-primary-800': props.isIncorrectGuess,
    'bg-primary-50 dark:bg-primary-800': !props.isCorrectGuess && !props.isIncorrectGuess,
  }
})

const textTheme = computed(() => {
  return {
    'text-secondary-300': props.isCorrectGuess,
    'text-primary-500': props.isIncorrectGuess,
    'text-primary-300': !props.isCorrectGuess && !props.isIncorrectGuess
  }
})

const themeTitle = computed(() => {
  return {
    'text-secondary-500/80': props.isCorrectGuess,
    'text-primary-500/50': props.isIncorrectGuess,
    'text-primary-300/50': !props.isCorrectGuess && !props.isIncorrectGuess
  }
})
</script>
