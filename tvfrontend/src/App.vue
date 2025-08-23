<template>
  <section id="interface" class="mx-5">
    <div class="px-5">
      <div v-if="isConnected && isVerified" class="grid grid-cols-5 grid-rows- gap-5 text-center my-20">
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

      <connection-block v-else @check-code="(code) => checkPinCode(code)" />
    </div>

    <!-- Modals -->
    <volt-dialog v-model:visible="showAnswer" :modal="true" class="w-[400px]">
      <div class="text-center">
        <h1 class="font-bold text-3xl mb-1">
          Mariah Carey
        </h1>
        <p class="font-light text-2xl">
          We belong together
        </p>
      </div>
    </volt-dialog>

    <!-- Audio -->
    <audio ref="audioEl">
      <source src="/win.mp3" type="audio/mpeg">
    </audio>
  </section>
</template>

<script setup lang="ts">
import { useGameTimer, useGameWebsocket } from '@/composables'
import 'animate.css'

const teamOneEl = useTemplateRef('teamOneEl')
const teamTwoEl = useTemplateRef('teamTwoEl')

const { connect, checkPinCode, showAnswer, isConnected, wsObject, isVerified } = useGameWebsocket()
const { timerMinutes, timerSeconds } = useGameTimer()

onMounted(() => {
  connect()
  document.body.classList.add('h-screen', 'bg-no-repeat', 'bg-gradient-to-b', 'from-primary-100', 'to-primary-50')
})

onUnmounted(() => {
  document.body.classList.remove('h-screen', 'bg-no-repeat', 'bg-gradient-to-b', 'from-primary-100', 'to-primary-50')
})
</script>
