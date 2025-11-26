<template>
  <transition mode="in-out" enter-active-class="animate__animated animate__fadeInLeftBig" leave-active-class="animate__animated animate__fadeOutRight">
    <div id="randomizer" v-if="show" class="absolute z-50 top-3/12 left-6/16 w-auto shadow-2xl h-auto bg-primary-50 rounded-xl p-2">
      <div class="p-2 flex justify-end">
        <volt-button @click="show=false">
          <vue-icon icon="lucide:eye-off" />
        </volt-button>
      </div>

      <div class="floor grid grid-cols-3 p-20 gap-1 hover:bg-primary-100/20 transition-all ease-in-out duration-500 rounded-xl cursor-pointer" @click="runRandomizer">
        <!-- :style="{ backgroundColor: detail.bgColor, color: detail.color }" -->
        <div v-for="detail in items" :key="detail.id" :class="{ 'bg-primary-300 text-surface-50': detail.value === squareName }" class="square text-center font-semibold p-5 bg-primary-200 text-surface rounded-lg cursor-pointer hover:bg-primary-200">
          <span>{{ detail.value }}</span>
        </div>
      </div>
    </div>
  </transition>
</template>

<script lang="ts" setup>
import { useSound } from '@vueuse/sound'
import type { RandomizerData } from '.'

const props = defineProps<{ show?: boolean, items: RandomizerData[], returnObject?: boolean, mute?: boolean }>()
const emit = defineEmits<{ completed: [value: string | RandomizerData | undefined] }>()

const show = useVModel(props, 'show', emit, { defaultValue: false, eventName: 'update:show' })


/**
 * Audio
 */

const { play } = useSound('/tick.mp3', { soundEnabled: !props.mute, volume: 0.5 })

/**
 * State
 */

const isSpinning = ref(false)
const squareName = ref<string>('')

// Run the randomizer animation
function runRandomizer() {
  if (isSpinning.value) {
    return
  }

  isSpinning.value = true

  const iterations = 20
  const finalSelection = Math.floor(Math.random() * props.items.length)

  let speed = 100
  let currentIteration = 0

  function animate() {
    // Animate the grid as long as the
    // iteration count is below "iterations"
    if (currentIteration < iterations) {
      // Ensures that we loop back to a square if the count goes
      // over the total number of available squares
      const currentIndex = currentIteration % props.items.length
      squareName.value = props.items[currentIndex].value

      // playTickSound()
      play()

      // speed += currentIteration / 2 // Decreseases speed at the end
      speed += (currentIteration / 2) * (currentIteration > 15 ? 2 : 1) // Increases speed at the end
      currentIteration++
      setTimeout(animate, speed)
    } else {
      // Once the iteration is complete, show the final
      // selected result
      squareName.value = props.items[finalSelection].value
      isSpinning.value = false
    }
  }

  animate()

  if (props.returnObject) {
    const item = props.items.find(x => x.value === squareName.value)
    emit('completed', item)
  } else {
    emit('completed', props.items[finalSelection].value)
  }
}

defineExpose({ runRandomizer })
</script>

<style lang="scss" scoped>
// $grid_size: 3;
// $hover_color: var(--color-primary-200);
// $highlight_color: var(--color-primary-100);

// .floor {
//   display: grid;
//   grid-template-columns: repeat($grid_size, 1fr);
//   border: 5px var(--color-border) solid;

//   .square {
//     transition: all .14s ease-in-out;
//     width: auto;
//     height: auto;
//     padding: 1rem;
//     display: flex;
//     flex-direction: column;
//     align-items: center;
//     justify-content: center;
//     text-align: center;
//     // border: 1px black solid;
//     cursor: pointer;

//     border-right: 1px solid var(--color-primary-800);
//     border-bottom: 1px solid var(--color-primary-800);

//     // Remove right border for every 3rd square (last in row)
//     &:nth-child(3n) {
//       border-right: none;
//     }

//     // Remove bottom border for last row (last 3 squares)
//     &:nth-last-child(-n + 3) {
//       border-bottom: none;
//     }

//     &.spinning {
//       cursor: not-allowed;
//     }

//     &.highlight {
//       color: var(--color-primary-50);
//       background-color: $highlight_color;
//     }

//     &:hover {
//       background-color: $hover_color;
//     }
//   }
// }
</style>
