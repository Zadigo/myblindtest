<template>
  <div :class="{ 'bg-primary/20': hasAnsweredCorrectly }" class="w-full shadow-md rounded-md p-10 flex flex-col justify-center relative">
    <h1 class="text-2xl font-semibold mb-5">
      Team name {{ teamId }}
    </h1>

    <div :class="{ 'animate__heartBeat': hasAnsweredCorrectly }" class="animate__animated bg-blue-100 w-2/4 p-10 rounded-xl font-bold self-center mb-10 animate__animated">
      <span class="text-5xl">300</span>
    </div>

    <p class="font-bold text-center mb-3">
      Consecutive answers
    </p>

    <div class="consecutive-answers w-2/4 h-auto self-center flex justify-around gap-2">
      <div v-for="i in 5" :key="i" :class="{ 'bg-green-300': i <= consecutiveAnswers, 'bg-gray-100': i > consecutiveAnswers }" class="answer p-4 rounded-md w-10" />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ correctAnswer?: number, teamId: number }>()

const consecutiveAnswers = ref<number>(3)

const hasAnsweredCorrectly = computed(() => {
  if (props.correctAnswer) {
    return props.correctAnswer === props.teamId
  } else {
    return false
  }
})
</script>
