<template>
  <section id="blindtest">
    <blind-test-layout>
      <template #video>
        <video-block />
      </template>
  
      <template #leftTeam>
        <team-block :team-index="0" />
      </template>
  
      <template #rightTeam>
        <team-block :team-index="1" />
      </template>
    </blind-test-layout>

    <!-- Modals -->
    <active-game v-model="warnActiveGameModal" @proceed="() => stopGame(stopGameCallback)" />
  </section>
</template>

<script setup lang="ts">
import { onBeforeRouteLeave, useRouter } from 'vue-router'

/**
 * Websocket
 */

const { currentSettings } = useSession()
const { wsObject, gameStarted, stopGame } = useGameWebsocket()

whenever(() => isDefined(currentSettings), () => {
  wsObject.open()
})

/**
 * Before leave
 */

const router = useRouter()
const warnActiveGameModal = ref(false)

onBeforeRouteLeave(() => {
  if (gameStarted.value) {
    warnActiveGameModal.value = true
    return false
  }
})

function stopGameCallback() {
  warnActiveGameModal.value = false
  router.push({ name: 'home' })
}

/**
 * SEO
 */

useHead({
  title: 'Blindtest',
  meta: [
    {
      name: 'description',
      content: 'Play an exciting blindtest game with your friends! Guess the songs and compete for the highest score.'
    }
  ]
})

</script>
