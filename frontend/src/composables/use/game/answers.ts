import type { BlindtestPlayer, Empty } from '@/types'

/**
 * Composable that calculates the number of
 * consecutive correct answers for a given player
 *
 * @param player The player to check for consecutive answers
 * @param callback Optional callback to execute when the player has enough consecutive answers
 * @param minConsecutive Minimum number of consecutive answers required to trigger the callback
 */
export function useConsecutiveAnswers(player: ComputedRef<Empty<BlindtestPlayer>> | Ref<Empty<BlindtestPlayer>>, callback?: () => void, minConsecutive = 3) {
  const songsStore = useSongs()
  const { correctAnswers } = storeToRefs(songsStore)

  /**
   * Computed properties
   */

  const consecutiveAnswers = computed(() => {
    if (correctAnswers.value.length < minConsecutive) return 0
    if (!isDefined(player)) return 0

    let count = 0

    for (let i = correctAnswers.value.length - 1; i >= 0; i--) {
      const answer = correctAnswers.value[i]

      if (answer && (answer.playerId === player.value.id)) {
        count++
      } else {
        break
      }
    }

    return count >= minConsecutive ? count : 0
  })

  /**
   * State
   */

  const hasConsecutiveAnswers = computed(() => consecutiveAnswers.value > minConsecutive)

  whenever(hasConsecutiveAnswers, () => { callback?.() })

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
