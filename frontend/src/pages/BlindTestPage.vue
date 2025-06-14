<template>
  <BlindTestLayout>
    <template #teamOne>
      <TeamBlock :team-index="0" class="bg-primary/40" @next-song="handleCorrectAnswer" />
    </template>

    <template #teamTwo>
      <TeamBlock :team-index="1" block-position="ms-auto" class="bg-primary/20" @next-song="handleCorrectAnswer" />
    </template>

    <template #video>
      <VideoBlock ref="videoEl" />
    </template>
  </BlindTestLayout>
</template>

<script setup lang="ts">
import VideoBlock from '@/components/blindtest/VideoBlock.vue'
import type { MatchedPart } from '@/data'
import type { VideoBlockExposedMethods } from '@/types'

useHead({
  title: 'Blindtest'
})

const songsStore = useSongs()
const { currentSong, correctAnswers, answers } = storeToRefs(songsStore)

const videoEl = useTemplateRef<InstanceType<typeof VideoBlock> & VideoBlockExposedMethods>('videoEl')

/**
 * Callback function that handles the correct
 * answser from a given team
 *
 * @param data The data to push
 */
function handleCorrectAnswer(data: [ teamId: string, match: MatchedPart ]) {
  if (currentSong.value) {
    correctAnswers.value.push({
      teamId: data[0],
      song: currentSong.value
    })

    console.log('handleCorrectAnswer', videoEl.value)

    if (videoEl.value) {
      videoEl.value.handleCorrectAnswer(data[0], data[1])

      answers.value.push({
        teamId: data[0],
        matched: data[1],
        song: currentSong.value
      })
    }
  }
}
</script>
