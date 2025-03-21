<template>
  <section id="interface" class="mx-5">
    <button type="button" class="p-4 shadow-sm bg-blue-500" @click="handleCorrectAnswer">
      Show answer
    </button>
    <div class="px-5 my-10">
      <div v-if="ws.status.value==='OPEN'" class="grid grid-cols-5 grid-rows- gap-5 text-center">
        <!-- Team 1 -->
        <TeamBlock ref="teamOneEl" :team-id="1" :correct-answer="correctAnswer" class="col-span-2" />

        <!-- Timer -->
        <div class="grid grid-flow-col grid-rows-3 gap-1">
          <div id="timer" class="shadow-none bg-black rounded-md flex justify-center place-items-center row-start-1">
            <span class="font-semibold text-3xl text-white block text-center">
              {{ timerMinutes }}:{{ timerSeconds }}
            </span>
          </div>
        </div>
        
        <!-- Team 2 -->
        <TeamBlock :team-id="2" :correct-answer="correctAnswer" class="col-span-2" />
      </div>

      <div v-else class="w-full flex justify-center">
        <div class="bg-white shadow-md rounded-md p-10 w-2/5">
          <form class="flex flex-col" @submit.prevent>
            <input type="text" class="bg-slate-100 rounded-sm w-full p-6 mb-4" placeholder="Code de connection">
            <button type="button" class="p-4 shadow-sm bg-blue-400 rounded-md place-self-end text-white uppercase font-semibold cursor-pointer transition-all hover:bg-blue-500">
              Se connecter
            </button>
          </form>
        </div>
      </div>
    </div>

    <!-- Backdrop -->
    <div v-if="showAnswer" id="backdrop" class="absolute top-0 left-0 z-40 bg-black flex justify-center h-full w-full opacity-40 transition-all ease-in-out" @click="showAnswer=false" />

    <!-- Answer -->
    <div v-if="showAnswer" id="correct-answer" class="absolute top-1/4 left-1/4 bg-white w-auto rounded-md p-10 text-3xl font-semibold text-center z-50 shadow-md">
      Mariah Carey - What about us
    </div>

    <!-- Audio -->
    <audio ref="audioEl">
      <source src="/win.mp3" type="audio/mpeg">
    </audio>
  </section>
</template>

<script setup lang="ts">
import 'animate.css'
import { onBeforeUnmount, ref } from 'vue'
import { useWebSocket, whenever } from '@vueuse/core'

import TeamBlock from '@/components/TeamBlock.vue'

interface WebsocketMessage {
  type: string
}

const teamOneEl = ref<HTMLElement>()
const audioEl = ref<HTMLAudioElement>()
const dissapearCountdown = ref()
const correctAnswer = ref<number | null>(null)
const showAnswer = ref(false)

const timerTotalSeconds = ref(120)
const timerIsRunning = ref(false)
const timerMinutes = ref<number>(2)
const timerSeconds = ref<number>(0)
let timerInterval: ReturnType<typeof setInterval> | null

whenever(() => showAnswer.value, () => {
  if (audioEl.value) {
    audioEl.value.play()
  }

  dissapearCountdown.value = setTimeout(() => {
    showAnswer.value = false
    correctAnswer.value = null
  }, 3000);
})

function handleResetTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerTotalSeconds.value = 120;
    timerMinutes.value = 2;
    timerSeconds.value = 0;
    timerIsRunning.value = false;
  }
}

function handleStartTimer() {
  if (timerIsRunning.value && timerTotalSeconds.value <= 0) {
    return
  } else {

    timerIsRunning.value = true
    
    timerInterval = setInterval(() => {
      timerSeconds.value--

      timerMinutes.value = Math.floor(timerSeconds.value / 60)
      timerSeconds.value = timerTotalSeconds.value % 60

      if (timerTotalSeconds.value <= 0) {
        if (timerInterval) {
          clearInterval(timerInterval)
          timerIsRunning.value = false
        }
      }
    })
  }
}

function handleOnConnected() {

}

function handleOnError() {

}

function handleOnDisconnected() {

}

function handleOnMessage(ws: WebSocket, event: MessageEvent<WebsocketMessage>) {
  console.log(ws, event)

  if (event.data.type ===  'gooele') {
    // Do something
    handleStartTimer()
  }
}

function handleCorrectAnswer() {
  correctAnswer.value = Math.floor(Math.random() * 2) + 1;
  showAnswer.value = true
}

const ws = useWebSocket('http://example.com/ws/', {
  immediate: false,
  onConnected: handleOnConnected,
  onError: handleOnError,
  onDisconnected: handleOnDisconnected,
  onMessage: handleOnMessage
})

onBeforeUnmount(() => {
  handleResetTimer()
})
</script>
