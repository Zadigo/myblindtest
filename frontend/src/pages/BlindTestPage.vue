<template>
  <BlindTestLayout>
    <template #teamOne>
      <TeamBlock :team-index="0" :margin-right="10" @next-song="handleCorrectAnswer" @team:settings="handleTeamSelection" />
    </template>
    
    <template #teamTwo>
      <TeamBlock :team-index="1" :margin-left="10" @next-song="handleCorrectAnswer" @team:settings="handleTeamSelection" />
    </template>

    <template #video>
      <VideoBlock ref="videoEl" @game:settings="showGameSettings=true" />
    </template>

    <template #default>
      <!-- <GameSettings v-model="showGameSettings" /> -->
      <TeamSettings v-model="showTeamSettings" :team-id="selectedTeamId" :update:team="handleUpdateTeam" />
    </template>
  </BlindTestLayout>
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs';
import { MatchedElement } from '@/types';
import { storeToRefs } from 'pinia';
import { useHead } from 'unhead';
import { ref } from 'vue';

import TeamBlock from '@/components/blindtest/TeamBlock.vue';
import VideoBlock from '@/components/blindtest/VideoBlock.vue';
import TeamSettings from '@/components/modals/TeamSettings.vue';
import BlindTestLayout from '@/layouts/BlindTestLayout.vue';

useHead({
  title: 'Blind test'
})

const songsStore = useSongs()
const { currentSong, correctAnswers } = storeToRefs(songsStore)

const showGameSettings = ref(false)
const showTeamSettings = ref(false)
const selectedTeamId = ref<string>('')
const videoEl = ref<HTMLElement>()

// Callback function that handles the correct
// answser from a given team
function handleCorrectAnswer (data: (string | MatchedElement)[]) {
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
function handleTeamSelection (teamId: string) {
  selectedTeamId.value = teamId
  showTeamSettings.value = true
}

// Handles updating the details for a
// given team
function handleUpdateTeam (value: string) {
  if (songsStore.cache) {
    const team = songsStore.cache.teams.find(x => x.id === value)
    if (team) {
      team.name = value
    }
  }
}
</script>
