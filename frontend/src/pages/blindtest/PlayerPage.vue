<template>
  <div class="relative h-screen w-full bg-no-repeat bg-center bg-cover bg-clip-content overflow-hidden" :style="{ backgroundImage: `url(${backgroundImage})` }">
    <volt-container size="sm">
      <div class="absolute top-4/12 left-1/2 transform -translate-x-1/2 z-50">
        <guess-state v-if="showAnswer" :is-correct-guess="isCorrectGuess" :is-incorrect-guess="isIncorrectGuess" :correct-song="correctSong" class="mt-5" />
        <main-card v-else :player="player" :is-ready="isReady" @toggle-settings-modal="toggleSettingsModal" />
      </div>

      <!-- Overlay -->
      <div :class="overlayTheme" class="absolute top-0 left-0 w-full h-screen opacity-90 z-1 blur-sm" />

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


/**
 * Ranking
 */


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
      'bg-linear-to-b from-primary-200 via-primary-300 to-primary-500 dark:from-primary-400 dark:via-primary-700 dark:to-primary-800': isIncorrectGuess.value,
      'bg-linear-to-b from-secondary-200 via-secondary-300 to-secondary-500 dark:from-secondary-400 dark:via-secondary-700 dark:to-secondary-800': isCorrectGuess.value
    }
  ]
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
