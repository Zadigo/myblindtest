<template>
  <div class="relative h-screen w-full overflow-hidden transition-all ease-in">
    <!-- Acton Bar -->
     <top-action-bar @toggle-graph="toggleShowGraph" />

    <!-- Content -->
    <volt-container size="sm">
      <div class="absolute top-50 left-1/2 transform -translate-x-1/2 z-50">
        <transition mode="out-in" enter-from-class="animate-zoomout opacity-0" enter-active-class="" enter-to-class="animate-zoomin opacity-100" leave-from-class="animate-zoomin opacity-100" leave-active-class="" leave-to-class="animate-zoomout opacity-0">
          <guess-state v-if="showAnswer" :is-correct-guess="isCorrectGuess" :is-incorrect-guess="isIncorrectGuess" :correct-song="correctSong" class="mt-5" />
          <template v-else>
            <ranking-state v-if="showGraph" />
            <main-card v-else :player="player" :is-ready="isReady" @toggle-settings-modal="toggleSettingsModal" />
          </template>
        </transition>
      </div>

      <!-- Background -->
      <div ref="bgEl" :class="bgTheme" class="absolute top-0 left-0 w-full h-screen bg-no-repeat bg-center bg-cover bg-fixed overflow-hidden" :style="{ backgroundImage: `url(${backgroundImage})` }"></div>

      <!-- Overlay -->
      <div ref="overlayEl" :class="overlayTheme" id="overlay" class="absolute top-0 left-0 w-full h-screen opacity-90 z-10" />

      <!-- Modals -->
      <volt-dialog v-model:visible="showSettingsModal">
        <template #header>
          <h2 class="text-2xl font-bold">Settings</h2>
        </template>

        <form v-if="player">
          <volt-input-text v-model="playerName" placeholder="Name" />
        </form>

        <template #footer>
          <volt-button @click="() => toggleSettingsModal()">
            Close
          </volt-button>
        </template>
      </volt-dialog>
    </volt-container>
  </div>

</template>

<script setup lang="ts">
import { doc, updateDoc } from 'firebase/firestore'
import { useFirestore } from 'vuefire'

/**
 * Websocket
 */

const { wsObject, player, isReady, showAnswer, players, backgroundImage, isCorrectGuess, isIncorrectGuess, correctSong } = useGameWebsocketIndividualPlayer()
wsObject.open()

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

const playerName = ref<string>('')
const { history } = useRefHistory(playerName)

const route = useRoute()
const { stringify } = useWebsocketMessage()

watchDebounced(playerName, async (newName) => {
  const docRef = doc(useFirestore(), 'blindtests', route.params.id)
  await updateDoc(docRef, { [`players.${player.value?.id}.name`]: newName  })
  wsObject.send(stringify({ action: 'update_player', id: player.value?.id, name: newName }))
}, { debounce: 2000 })

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
