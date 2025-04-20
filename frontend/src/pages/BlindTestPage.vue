<template>
  <BlindTestLayout>
    <template #teamOne>
      <TeamBlock :team-index="0" class="bg-blue-200" @next-song="handleCorrectAnswer" @team-settings="handleTeamSelection" />
    </template>

    <template #teamTwo>
      <TeamBlock :team-index="1" block-position="ms-auto" class="bg-yellow-200" @next-song="handleCorrectAnswer" @team-settings="handleTeamSelection" />
    </template>

    <template #video>
      <VideoBlock ref="videoEl" />
    </template>
  </BlindTestLayout>
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs'
import { MatchedElement } from '@/types'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'

import TeamBlock from '@/components/blindtest/TeamBlock.vue'
import VideoBlock from '@/components/blindtest/VideoBlock.vue'
import BlindTestLayout from '@/layouts/BlindTestLayout.vue'

const songsStore = useSongs()
const { currentSong, correctAnswers } = storeToRefs(songsStore)

const showTeamSettings = ref(false)
const selectedTeamId = ref<number>()
const videoEl = ref<HTMLElement>()

/**
 * Callback function that handles the correct
 * answser from a given team
 */
function handleCorrectAnswer(data: (number | MatchedElement)[]) {
  if (songsStore.cache) {
    if (currentSong.value && data) {
      correctAnswers.value.push({
        teamId: data[0],
        song: currentSong.value
      })

      if (videoEl.value) {
        // videoEl.value.handleNextSong()
        videoEl.value.handleCorrectAnswer(data[0], data[1])
      }
    }
  } else {
    console.error('handleCorrectAnswer: BlindTestPage')
  }
}

// Function that sets the team to edit
function handleTeamSelection(teamId: number) {
  selectedTeamId.value = teamId
  showTeamSettings.value = true
}

// Handles updating the details for a
// given team
// function handleUpdateTeam (value: string) {
//   if (songsStore.cache) {
//     const team = songsStore.cache.teams.find(x => x.id === value)
//     if (team) {
//       team.name = value
//     }
//   }
// }
</script>
