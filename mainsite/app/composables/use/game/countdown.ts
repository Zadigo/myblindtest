import { useSound } from '@vueuse/sound'

/**
 * Composable that provides a countdown timer
 * for the game based on the time limit
 * set in the game settings
 * @param callback Optional callback to execute when the timer stops
 */
export const useGameCountdown = createGlobalState((callback?: () => void) => {
  const { gameStarted } = useAdminWebsocket()

  const { currentSettings } = useSession()
  const _timerValue = toValue(currentSettings.value?.settings.timeLimit)

  console.log('time value', _timerValue)

  /**
   * Countdown timer
   */

  const timeLimit = ref<number>(isDefined(_timerValue) ? _timerValue * 60 : 0)
  const { remaining, isActive, start, pause, reset } = useCountdown(timeLimit, { 
    immediate: false, 
    interval: 1000
  })

  watchDebounced(gameStarted, (newVal) => {
    if (newVal) {
      start()
    } else {
      pause()
      reset()
      callback?.()
    }
  }, { 
    debounce: 300
  })

  /**
   * Convert remaining time to minutes:seconds format
   */

  const timerToMinutes = computed(() => {
    const minutes = Math.floor(remaining.value / 60)
    const seconds = remaining.value % 60

    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  })

  /**
   * State
   */

  const hasTimer = computed(() => isDefined(_timerValue) && _timerValue > 0)


  /**
   * Watchers
   */

  const lessThanFiveSeconds = computed(() => isActive.value && remaining.value <= 5 && gameStarted.value)
  const lessThanTenSeconds = computed(() => isActive.value && remaining.value > 5 && remaining.value <= 10 && gameStarted.value)

  /**
   * Play sound when less than 10 seconds remain
   */

  const { play, stop } = useSound('/clock.mp3', { volume: 0.5 })

  whenever(lessThanTenSeconds, (state) => {
    if (state) {
      play()
    } else {
      stop()
    }
  })

  /**
   * Utilities
   */

  function restart() {
    if (gameStarted.value) {
      pause()
      reset()
      start()
    }
  }

  tryOnBeforeUnmount(() => {
    restart()
  })

  return {
    /**
     * Remaining time in seconds
     * @default 0
     */
    remaining,
    /**
     * Whether the timer is active
     * @default false
     */
    isActive,
    /**
     * Time remaining in minutes and seconds
     * @default "0:00"
     */
    timerToMinutes,
    /**
     * Time limit in seconds
     * @default 0
     */
    timeLimit,
    /**
     * Whether a timer is set by the user
     * in the game settings
     * @default false
     */
    hasTimer,
    /**
     * Whether there are less than five seconds remaining
     * @default false
     */
    lessThanFiveSeconds,
    /**
     * Whether there are less than ten seconds remaining
     * @default false
     */
    lessThanTenSeconds,
    /**
     * Reset the timer to the initial value
     */
    restart
  }
})
