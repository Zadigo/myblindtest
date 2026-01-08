import type { BlindtestPlayer, Empty } from '~/types'

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
