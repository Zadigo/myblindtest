<template>
  <div class="absolute top-50 left-1/2 transform -translate-x-1/2 z-50">
    <transition mode="out-in" enter-from-class="animate-zoomout opacity-0" enter-active-class="" enter-to-class="animate-zoomin opacity-100" leave-from-class="animate-zoomin opacity-100" leave-active-class="" leave-to-class="animate-zoomout opacity-0">
      <blindtest-score-guess-state v-if="showAnswer" :is-correct-guess="isCorrectGuess" :is-incorrect-guess="isIncorrectGuess" :correct-song="correctSong" class="mt-5" />
      <template v-else>
        <blindtest-score-ranking-state v-if="showGraph" />
        <blindtest-score-main-card v-else :player="player" :is-ready="isReady" @toggle-settings-modal="toggleSettingsModal" />
      </template>
    </transition>

    <!-- Multiple Choices -->
    <player-multiple-choices class="mt-3 z-20" />

    <!-- Modals -->
    <player-modals-settings-modal v-model:show="showSettingsModal" :player="player" />
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'player'
})

/**
 * Websocket
 */

const { player, isReady, showAnswer, isCorrectGuess, isIncorrectGuess, correctSong } = usePlayerWebsocket()

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
 * Modals (Name Update)
 */

const [showSettingsModal, toggleSettingsModal] = useToggle()

/**
 * SEO
 */

useHead({
  title: 'Player - MyBlindTest',
  meta: [
    {
      name: 'keywords',
      content: 'blind test, music quiz, player, join game, compete, fun, multiplayer, MyBlindTest',
    }
  ]
})
</script>
