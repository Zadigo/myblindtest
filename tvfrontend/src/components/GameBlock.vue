<template>
  <div class="grid grid-cols-5 grid-rows- gap-5 text-center my-20">
    <!-- Team 1 -->
    <team-block ref="teamOneEl" :team-id="1" :correct-answer="correctAnswer" class="col-span-2" />

    <!-- Timer -->
    <div class="grid grid-flow-col grid-rows-3 gap-1">
      <div id="timer" class="shadow-none bg-black rounded-md flex justify-center place-items-center row-start-1">
        <span class="font-semibold text-3xl text-white block text-center">
          {{ timerMinutes }}:{{ timerSeconds }}
        </span>
      </div>
    </div>

    <!-- Team 2 -->
    <team-block ref="teamTwoEl" :team-id="2" :correct-answer="correctAnswer" class="col-span-2" />
  </div>
</template>

<script setup lang="ts">
const teamOneEl = useTemplateRef('teamOneEl')
const teamTwoEl = useTemplateRef('teamTwoEl')

const { timerMinutes, timerSeconds } = useGameTimer()

const correctAnswer = ref<number>(0)
</script>
