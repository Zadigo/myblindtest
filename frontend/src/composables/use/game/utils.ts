import { useSound } from '@vueuse/sound'
import type { MaybeRef } from 'vue'
import type { Empty, BlindtestPlayer } from '@/types'

/**
 * A composable function to handle animations
 * @param name The name of the element to animate
 * @returns A function to trigger the animation
 */
export function useAnimationComposable(name: string, animationClasses: string[] = []) {
  const tokens = animationClasses.length > 0 ? animationClasses : ['animate__animated', 'animate__heartBeat', 'animate__repeat-1']
  const el = useTemplateRef<HTMLElement>(name)

  async function handleAnimation() {
    if (isDefined(el)) {
      const animationClasses = tokens

      // First remove the classes if they exist
      el.value.classList.remove(...tokens)

      // Force a reflow to restart the animation
      void el.value.offsetWidth

      // Add the classes back
      el.value.classList.add(...animationClasses)
    }
  }

  return {
    /**
     * Function to trigger the animation
     */
    handleAnimation
  }
}

/**
 * Composable that calculates the number of
 * consecutive correct answers for a given team
 *
 * @param team The team to calculate for
 * @param minConsecutive The minimum number of consecutive answers to qualify
 */
export function useConsecutiveAnswers(player: MaybeRef<Empty<BlindtestPlayer>>, minConsecutive = 2) {
  const songsStore = useSongs()
  const { correctAnswers } = storeToRefs(songsStore)

  const consecutiveAnswers = computed(() => {
    if (correctAnswers.value.length < minConsecutive) {
      return 0
    }

    let count = 0

    for (let i = correctAnswers.value.length - 1; i >= 0; i--) {
      const answer = correctAnswers.value[i]

      if (answer && (answer.teamId === (player.value && player.value.id))) {
        count++
      } else {
        break
      }
    }

    return count >= minConsecutive ? count : 0
  })

  const hasConsecutiveAnswers = computed(() => consecutiveAnswers.value > minConsecutive)
  const currentBonus = ref<number>(0)

  whenever(hasConsecutiveAnswers, () => {
    // Do something
    currentBonus.value = 0
  })


  return {
    /**
     * The number of consecutive correct answers
     * for the given team
     */
    consecutiveAnswers,
    /**
     * Whether the team has enough consecutive
     * answers to qualify
     * @default false
     */
    hasConsecutiveAnswers
  }
}

/**
 * Composable that provides a countdown timer
 * for the game based on the time limit
 * set in the game settings
 * @param callback Optional callback to execute when the timer stops
 */
export const useGameCountdown = createGlobalState((callback?: () => void) => {
  const { gameStarted } = useGameWebsocketIndividual()

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
