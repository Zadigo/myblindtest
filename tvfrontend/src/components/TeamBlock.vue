<template>
  <div :class="{ 'bg-primary-100': hasAnsweredCorrectly, 'bg-primary-200': !hasAnsweredCorrectly }" class="w-full shadow-md rounded-md p-10 flex flex-col justify-center relative">
    <h1 class="text-2xl font-bold mb-5">{{ teamName }}</h1>

    <div :class="{ 'animate__heartBeat': hasAnsweredCorrectly }" class="animate__animated bg-primary-50 w-2/4 p-10 rounded-xl font-bold self-center mb-10">
      <span class="text-5xl">
        {{ team.score }}
      </span>
    </div>

    <p class="font-bold text-center mb-3">
      Réponses consécutives
    </p>

    <div class="h-auto self-center flex justify-around gap-2">
      <div v-for="i in 5" :key="i" :class="{ 'bg-green-300': i <= consecutiveAnswers, 'bg-primary-50': i > consecutiveAnswers }" class="p-4 rounded-md w-10" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Team } from '@/types/game'

const props = defineProps<{ correctAnswer?: number, team: Team }>()

const consecutiveAnswers = ref<number>(3)

const teamName = computed(() => {
  if (props.team) {
    return props.team.name || props.team.id
  } else {
    return 'Team XYZ'
  }
})

const hasAnsweredCorrectly = ref(false)
</script>
