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
 * @param startFrom Time to start the countdown from
 */
export const useGameCountdown = createGlobalState((startFrom: number | undefined) => {
  if (isDefined(startFrom)) {
    console.log(startFrom, typeof startFrom)
    const timeLimit = refDefault<number>(toRef(startFrom * 60), 0)
    const { gameStarted } = useGameWebsocketIndividual()
    const { remaining, start, pause, reset } = useCountdown(timeLimit, { immediate: false, interval: 1000 })
  
    const { play, stop } = useSound('/clock.mp3', { volume: 0.5 })

    const toMinutes = computed(() => {
      const minutes = Math.floor(remaining.value / 60)
      const seconds = remaining.value % 60
      return `${minutes}:${seconds.toString().padStart(2, '0')}`
    })
  
    whenever(() => remaining.value > 0 && remaining.value <= 10, (value) => {
      if (value) {
        play()
      } else {
        stop()
      }
    })
  
    watchDebounced(gameStarted, (state) => {
      if (state) {
        start()
      } else {
        pause()
        reset()
      }
    })
    return {
      toMinutes,
      timeLimit,
      remaining,
      start,
      pause,
      reset
    }
  } else {
    return {
      toMinutes: ref('0:00'),
      timeLimit: ref(0),
      remaining: ref(0),
      start: () => {},
      pause: () => {},
      reset: () => {}
    }
  }
})

