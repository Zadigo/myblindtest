<template>
  <new-layout>
    <template #video>
      <new-video-block />
    </template>

    <template #leftTeam>
      <new-team-block :team-index="0" />
    </template>

    <template #rightTeam>
      <new-team-block :team-index="1" />
    </template>
  </new-layout>
</template>

<script setup lang="ts">
/**
 * Wescocket
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
