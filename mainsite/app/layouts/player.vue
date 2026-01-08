<template>
  <div class="relative h-screen w-full overflow-hidden transition-all ease-in">
    <!-- Acton Bar -->
    <blindtest-score-top-action-bar @toggle-graph="toggleShowGraph" />

    <!-- Content -->
    <volt-container size="sm">
      <div class="relative h-screen w-full overflow-hidden transition-all ease-in">
        <slot />
      </div>
      <!-- Background -->
      <div ref="bgEl" :class="bgTheme" class="absolute top-0 left-0 w-full h-screen bg-no-repeat bg-center bg-cover bg-fixed overflow-hidden" :style="{ backgroundImage: `url(${backgroundImage})` }"></div>

      <!-- Overlay -->
      <div ref="overlayEl" :class="overlayTheme" id="overlay" class="absolute top-0 left-0 w-full h-screen opacity-90 z-10" />
    </volt-container>
  </div>
</template>

<script setup lang="ts">
/**
 * Websocket
 */

const { backgroundImage, isCorrectGuess, isIncorrectGuess } = usePlayerWebsocket()

/**
 * Background
 */

const bgEl = useTemplateRef<HTMLDivElement>('bgEl')
const { x, y } = useMouse({ touch: false })

watch([x, y], () => {
  if (bgEl.value) {
    const xPos = x.value / window.innerWidth * 10
    const yPos = y.value / window.innerHeight * 10

    bgEl.value.style.transform = `translate(-${xPos}%, -${yPos}%) scale(1.2)`
  }
})

/**
 * Ranking
 */

const showGraph = useLocalStorage('blindtest-show-graph', false)
const toggleShowGraph = useToggle(showGraph)

/**
 * Themes
 */

const overlayTheme = computed(() => {
  return [
    {
      'bg-linear-to-b from-primary-200 via-primary-300 to-primary-500 dark:from-primary-400 dark:via-primary-500 dark:to-primary-800': isIncorrectGuess.value,
      'bg-linear-to-tr from-secondary-200 via-secondary-300 to-secondary-500 dark:from-secondary-400 dark:via-secondary-700 dark:to-secondary-800': isCorrectGuess.value,
      'bg-linear-to-t from-neutral-200 to-neutral-700 dark:from-neutral-500 dark:to-neutral-900/50': !isCorrectGuess.value && !isIncorrectGuess.value,
    }
  ]
})

const bgTheme = computed(() => {
  return {
    'blur-xs': isCorrectGuess.value || isIncorrectGuess.value,
    'filter grayscale-50 brightness-50 blur-md': !isCorrectGuess.value && !isIncorrectGuess.value,
  }
})
</script>

<style scoped>
#overlay {
  animation: gradient 15s ease infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 0%;
  }

  50% {
    background-position: 100% 100%;
  }

  100% {
    background-position: 0% 0%;
  }
}
</style>
