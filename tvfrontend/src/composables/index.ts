import type { Ref } from 'vue'

export * from './game/ws_manager'

/**
 * Composable for managing game timer
 */
export function useGameTimer() {
  const timerTotalSeconds = ref<number>(120)
  const timerIsRunning = ref<boolean>(false)
  const timerMinutes = ref<number>(2)
  const timerSeconds = ref<number>(0)
  let timerInterval: ReturnType<typeof setInterval> | null

  function start() {
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

  function reset() {
    if (timerInterval) {
      clearInterval(timerInterval)
      timerTotalSeconds.value = 120
      timerMinutes.value = 2
      timerSeconds.value = 0
      timerIsRunning.value = false
    }
  }


  return {
    start,
    reset,
    timerTotalSeconds,
    timerIsRunning,
    timerMinutes,
    timerSeconds
  }
}

/**
 * Composable for handling audio animations
 */
export function useAudioAnimation(showAnswer: Ref<boolean>) {
  const audioEl = ref<HTMLAudioElement>()

  whenever(() => showAnswer.value, () => {
    if (audioEl.value) {
      audioEl.value.play()
    }
  })
}
