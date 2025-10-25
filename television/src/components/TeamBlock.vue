<template>
  <div :class="theme" class="w-full p-10 flex flex-col justify-center relative">
    <h1 class="text-2xl font-semibold mb-5">
      {{ teamName }}
    </h1>

    <div :class="{ 'animate__heartBeat': hasAnsweredCorrectly }" class="animate__animated bg-primary-100 dark:bg-primary-800 dark:text-surface-0 w-2/4 p-10 rounded-xl font-bold self-center mb-10">
      <span class="text-6xl">
        {{ team.score }}
      </span>
    </div>

    <p class="font-bold text-center mb-3">
      Réponses consécutives
    </p>

    <!-- <div class="h-auto self-center flex justify-around gap-2">
      <div v-for="i in 5" :key="i" :class="{ 'bg-green-300': i <= consecutiveAnswers, 'bg-primary-50': i > consecutiveAnswers }" class="p-4 rounded-md w-10" />
    </div> -->
  </div>
</template>

<script setup lang="ts">
import type { Team } from '@/types/game'

const props = defineProps<{ correctAnswer?: string, team: Team, position: 'left' | 'right' }>()

/**
 * Team
 */

const teamName = computed(() => isDefined(props.team) ? (props.team.name || props.team.id) : '-')

/**
 * Answers
 */

// const consecutiveAnswers = ref<number>(3)

const gameStore = useGameStore()
const { correctAnswerTeamId } = storeToRefs(gameStore)
const hasAnsweredCorrectly = computed(() => props.team.id === correctAnswerTeamId.value)

// animate-pulse duration-300
const theme = ref({ 
  'bg-primary-100': hasAnsweredCorrectly.value, 
  'bg-linear-to-l from-primary-300 to-primary-50': !hasAnsweredCorrectly.value && props.position === 'left',
  'bg-linear-to-l from-primary-50 to-primary-300': !hasAnsweredCorrectly.value && props.position === 'right',
})

</script>
