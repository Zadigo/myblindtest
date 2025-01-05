<template>
  <BlindTestLayout>
    <template #teamOne>
      <TeamBlock :team-id="0" :margin-right="10" @next-song="handleCorrectAnswer" @team:settings="handleTeamSelection" />
    </template>
    
    <template #teamTwo>
      <TeamBlock :team-id="1" :margin-left="10" @next-song="handleCorrectAnswer" @team:settings="handleTeamSelection" />
    </template>

    <template #video>
      <VideoBlock ref="videoEl" @game:settings="showGameSettings=true" />
    </template>

    <template #default>
      <GameSettings v-model="showGameSettings" />
      <TeamSettings v-model="showTeamSettings" :team-id="selectedTeam" :update:team="handleUpdateTeam" />
    </template>
  </BlindTestLayout>
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs';
import { storeToRefs } from 'pinia';
import { useHead } from 'unhead';
import { ref } from 'vue';

import TeamBlock from '@/components/blindtest/TeamBlock.vue';
import VideoBlock from '@/components/blindtest/VideoBlock.vue';
import GameSettings from '@/components/modals/GameSettings.vue';
import TeamSettings from '@/components/modals/TeamSettings.vue';
import BlindTestLayout from '@/layouts/BlindTestLayout.vue';

useHead({
  title: 'Blind test'
})

const songsStore = useSongs()
const { currentSong, correctAnswers } = storeToRefs(songsStore)

const showGameSettings = ref(false)
const showTeamSettings = ref(false)
const selectedTeam = ref<number>(0)
const videoEl = ref<HTMLElement>()

function handleCorrectAnswer (teamId: number) {
  if (songsStore.cache) {
    if (currentSong.value) {
      correctAnswers.value.push({
        teamId: teamId,
        song: currentSong.value
      })
    }

    if (videoEl.value) {
      videoEl.value.handleNextSong()
    }
  }
}

function handleTeamSelection (teamId: number) {
  selectedTeam.value = teamId
  showTeamSettings.value = true
}

function handleUpdateTeam (value: string) {
  if (songsStore.cache) {
    songsStore.cache.teams[selectedTeam.value].name = value
  }
}
</script>
