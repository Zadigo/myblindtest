<template>
  <div ref="teamBlockEl" class="p-5 h-screen relative">
    <div id="team" :class="blockPosition" class="flex-col w-7/12 absolute top-7/20 left-4/20">
      <volt-card class="w-full text-center border-none shadow-none">
        <template #content>
          <h1 ref="scoreBoxEl" class="text-6xl font-bold">
            {{ teamScore }}
          </h1>

          <p class="font-light uppercase text-sm">
            Points ({{ teamName }})
          </p>
        </template>
      </volt-card>

      <!-- Actions -->
      <volt-card class="mt-2 mb-10 border-none shadow-none">
        <template #content>
          <div class="flex justify-center gap-2">
            <volt-button :variant="matchedElement === 'Title' ? '' : 'outlined'" size="small" @click="handleMatch('Title')">
              <vue-icon icon="fa-solid:star-half" />
              Title
            </volt-button>

            <volt-button :variant="matchedElement === 'Artist' ? '' : 'outlined'" size="small" @click="handleMatch('Artist')">
              <vue-icon icon="fa-solid:star-half" />
              Artist
            </volt-button>

            <volt-button :variant="matchedElement === 'Both' ? '' : 'outlined'" size="small" @click="handleMatch('Both')">
              <vue-icon icon="fa-solid:star" />
              Both
            </volt-button>
          </div>

          <div class="flex justify-center mt-4 w-full">
            <volt-contrast-button :disabled="!gameStarted" class="w-10/13 self-center" @click="proxySendCorrectAnswer">
              <vue-icon icon="fa-solid:check" />
              Validate
            </volt-contrast-button>
          </div>
        </template>
      </volt-card>

      <div class="flex gap-1 justify-center p-5 mt-3">
        <div v-for="i in 5" :key="i" class="p-2 bg-brand-shade-5/50 rounded-md w-1/6" />
      </div>

      <!-- Consecutive Answers -->
      <Transition class="animate__animated" enter-to-class="animate__zoomInLeft" leave-to-class="animate__fadeOutLeft">
        <h1 v-if="hasConsecutiveAnswers" class="text-5xl font-bold text-gray-700">
          Exceptionnel x {{ consecutiveAnswers }}
        </h1>
      </Transition>

      <!-- Fireworks -->
      <base-fireworks v-show="gameStarted && hasConsecutiveAnswers" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useAnimationComposable, useConsecutiveAnswers } from '@/composables/use/game/utils';
import type { MatchedPart } from '@/data'

const emit = defineEmits<{ 'next-song': [data: [ teamId: string, match: MatchedPart]] }>()

const { teamIndex = 1, marginRight = 0, marginLeft = 0, diffusionMode = false, blockPosition = 'me-auto' } = defineProps<{ 
  teamIndex: number, 
  marginRight?: number, 
  marginLeft?: number, 
  diffusionMode?: boolean, 
  blockPosition?: string 
}>()

const songsStore = useSongs()
const { gameStarted } = storeToRefs(songsStore)

/**
 * Team
 */

const teamStore = useTeamsStore()
const { teams } = storeToRefs(teamStore)

const team = teamStore.getTeamByIndex(teamIndex)
const teamName = computed(() => {
  if (team.value) {
    return team.value.name === '' ? team.value.id : team.value.name
  } else {
    return 'Team XYZ'
  }
})

const teamScore = computed(() => team.value ? team.value.score : 0)

/**
 * Consecutive answers
 */

const { consecutiveAnswers, hasConsecutiveAnswers } = useConsecutiveAnswers(team, 2)

/**
 * Animations
 */

const { handleAnimation: handleTeamBlockAnimation } = useAnimationComposable('teamBlockEl')
const { handleAnimation: handleScoreAnimation } = useAnimationComposable('scoreBoxEl')

/**
 * Answering
 */

const matchedElement = ref<MatchedPart>('Both')
const { sendCorrectAnswer } = useGameWebsocket()

async function proxySendCorrectAnswer() {
  if (team.value) {
    await handleTeamBlockAnimation()
    await handleScoreAnimation()
    
    console.log('Correct answer', team.value)

    sendCorrectAnswer(team.value.id, matchedElement.value)
    matchedElement.value = 'Both'
  } else {
    console.error('handleCorrectAnswer', 'No team')
  }
}

function handleMatch(match: MatchedPart) {
  matchedElement.value = match
}
</script>
