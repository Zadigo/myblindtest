<template>
  <section id="interface" class="mx-5">
    <div class="px-5">
      <div v-if="isConnected" class="grid grid-cols-5 grid-rows- gap-5 text-center my-20">
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
        <TeamBlock ref="teamTwoEl" :team-id="2" :correct-answer="correctAnswer" class="col-span-2" />
      </div>

      <ConnectionBlock v-else @connect-client="handleConnection" />
    </div>

    <Dialog v-model:open="showAnswer">
      <DialogContent>
        <div class="text-center">
          <h1 class="font-bold text-3xl mb-3">
            Mariah Carey
          </h1>
          <p class="font-light text-2xl">
            We belong together
          </p>
        </div>
      </DialogContent>
    </Dialog>

    <!-- Audio -->
    <audio ref="audioEl">
      <source src="/win.mp3" type="audio/mpeg">
    </audio>
  </section>
</template>

<script setup lang="ts">
import 'animate.css'
import { toast } from 'vue-sonner'

interface WebsocketMessage {
  type: string
}

const { sendMessage } = useWebsocketUtilities()

const teamOneEl = useTemplateRef('teamOneEl')
const teamTwoEl = useTemplateRef('teamTwoEl')

const audioEl = ref<HTMLAudioElement>()

const dissapearCountdown = ref()
const correctAnswer = ref<number | null>(null)
const showAnswer = ref<boolean>(false)

const timerTotalSeconds = ref<number>(120)
const timerIsRunning = ref<boolean>(false)
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
  }, 3000)
})

/**
 *
 */
function handleResetTimer() {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerTotalSeconds.value = 120
    timerMinutes.value = 2
    timerSeconds.value = 0
    timerIsRunning.value = false
  }
}

/**
 *
 */
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

/**
 *
 */
function handleOnConnected() {

}

/**
 *
 */
function handleOnError() {
  toast('Failed to connect to websocket', {
    position: 'top-center'
  })
}

/**
 *
 */
function handleOnDisconnected() {

}

/**
 * @param ws Websocket
 * @param event The incoming event
 */
function handleOnMessage(ws: WebSocket, event: MessageEvent<WebsocketMessage>) {
  console.log(ws, event)

  if (event.data.action === 'google') {
    // Do something
    handleStartTimer()
  }
}

const ws = useWebSocket(getWebsocketUrl('/ws/connect'), {
  immediate: false,
  onConnected: handleOnConnected,
  onError: handleOnError,
  onDisconnected: handleOnDisconnected,
  onMessage: handleOnMessage
})

const isConnected = computed(() => ws.status.value === 'OPEN')

/**
 * Connec to Django
 *
 * @param code The code for the current blindtest session
 */
function handleConnection(code: string) {
  ws.open()
  ws.send(sendMessage<{ action: string, code: string }>({ action: 'check_code', code: code }))
}

onBeforeUnmount(() => {
  handleResetTimer()
})
</script>
