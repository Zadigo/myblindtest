import type { Empty, Team } from '@/types'
import type { MaybeRef } from 'vue'

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
 * Composable used to handle game-related
 * websocket messages
 */
export const useGameComposable = createSharedComposable(() => {
  const { stringify } = useWebsocketMessage()
  const wsManager = useGameWebsocket()

  const songsStore = useSongs()
  // const { gameStarted, currentSong, currentStep, correctAnswers } = storeToRefs(songsStore)

  /**
   * Callback function used after a correct or
   * incorrect answer was triggered
   */
  function handleFinalize() {
    songsStore.incrementStep()
  }

  function sendIncorrectAnswer() {
    const result = stringify({ action: 'skip_song' })

    if (result) {
      wsManager.wsObject.send(result)
      handleFinalize()
    }
  }

  function sendCorrectAnswer(teamId: string, match: MatchedPart) {
    let title_match = true
    let artist_match = true

    if (match === 'Title') {
      title_match = true
      artist_match = false
    }

    if (match === 'Artist') {
      title_match = false
      artist_match = true
    }

    const result = stringify({
      action: 'submit_guess',
      team_id: teamId,
      title_match,
      artist_match
    })

    console.log('handleCorrectAnswer', result)

    if (result) {
      wsManager.wsObject.send(result)
      handleFinalize()
    }
  }

  return {
    /**
    * Returns the next song by excluding
    * those that were already played
    * 
    * @param teamId The ID of the team
    * @param match The element that was matched
    */
    sendIncorrectAnswer,
    /**
     * Proxy function that can be used by parent elements
     * to trigger a websocket message on the team guess
     *
     * @param teamId The ID of the team
     * @param match The element that was matched
     */
    sendCorrectAnswer
  }
})

/**
 * Composable that calculates the number of
 * consecutive correct answers for a given team
 *
 * @param team The team to calculate for
 */
export function useConsecutiveAnswers(team: MaybeRef<Empty<Team>>, minConsecutive = 2) {
  const songsStore = useSongs()
  const { correctAnswers } = storeToRefs(songsStore)

  const consecutiveAnswers = computed(() => {
    if (correctAnswers.value.length < minConsecutive) {
      return 0
    }

    let count = 0

    for (let i = correctAnswers.value.length - 1; i >= 0; i--) {
      const answer = correctAnswers.value[i]

      if (answer && (answer.teamId === (team.value && team.value.id))) {
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
