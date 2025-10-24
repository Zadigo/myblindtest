<template>
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
</template>

<script setup lang="ts">
/**
 * Websocket
 */

const { currentSettings } = useSession()
const { wsObject } = useGameWebsocket()

whenever(() => isDefined(currentSettings), () => {
  wsObject.open()
})

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
