<template>
  <BlindTestLayout>
    <template #teamOne>
      <TeamBlock :team-index="0" class="bg-blue-200" @next-song="handleCorrectAnswer" />
    </template>

    <template #teamTwo>
      <TeamBlock :team-index="1" block-position="ms-auto" class="bg-yellow-200" @next-song="handleCorrectAnswer" />
    </template>

    <template #video>
      <VideoBlock ref="videoEl" />
    </template>
  </BlindTestLayout>
</template>

<script setup lang="ts">
import type { MatchedPart } from '@/types'

const songsStore = useSongs()
const { currentSong, correctAnswers } = storeToRefs(songsStore)

const videoEl = ref<HTMLElement>()

/**
 * Callback function that handles the correct
 * answser from a given team
 *
 * @param (number | string)[]
 */
function handleCorrectAnswer(data: (number | MatchedPart)[]) {
  if (songsStore.cache) {
    if (currentSong.value && data) {
      correctAnswers.value.push({
        teamId: data[0],
        song: currentSong.value
      })

      if (videoEl.value) {
        videoEl.value.handleCorrectAnswer(data[0], data[1])
      }
    }
  } else {
    console.error('handleCorrectAnswer: BlindTestPage')
  }
}
</script>
