<template>
  <div class="answer absolute bg-primary-100 h-auto w-auto shadow-lg left-[calc(50%-280px)] rounded-lg bg-primary-600 flex flex-col justify-center items-center text-surface-0 p-20">
    <h2 class="text-8xl font-bold">{{ answer?.name || 'Correct Answer' }}</h2>
    <p class="text-3xl">{{ answer?.artist.name || 'Unknown Title' }}</p>
    <p>{{ correctAnswerTeamId || '-' }}</p>
  </div>
</template>

<script setup lang="ts">
const gameStore = useGameStore()
const { answer, correctAnswerTeamId } = storeToRefs(gameStore)

const { css } = useStyleTag(`
  .answer {
    background-image: url("https://i.scdn.co/image/fe0085416276eb64c28eda1d2ef1feecbaa16d60");
    background-blend-mode: screen;
    background-size: cover;
    background-position: center;
  }
`)

css.value = `
  .answer {
    background-image: url("${answer.value?.artist.spotify_avatar}");
    background-blend-mode: screen;
    background-size: cover;
    background-position: center;
  }
`
</script>
