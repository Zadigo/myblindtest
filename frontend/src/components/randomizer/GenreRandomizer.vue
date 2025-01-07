<template>
  <div class="card shadow-none">
    <div class="card-body">
      <div class="floor" @click="runRandomizer">
        <div v-for="detail in items" :key="detail.id" :class="{highlight: detail.value === squareName}" class="square">
          <span>{{ detail.value }}</span>
        </div>
      </div>
    </div>

    <!-- Audio -->
    <audio id="tickSound" preload="auto">
      <source src="/tick.mp3" type="audio/mp3">
    </audio>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, PropType, ref } from 'vue';
import { RandomizerData } from '.';

const emit = defineEmits({
  completed (_value: string | RandomizerData | undefined) {
    return true
  }
})

const props = defineProps({
  items: {
    type: Object as PropType<RandomizerData[]>,
    required: true
  },
  returnObject: {
    type: Boolean
  },
  mute: {
    type: Boolean
  }
})

// Audio elements
const tickSound = ref<HTMLAudioElement | null>(null);
const isSpinning = ref(false)
const squareName = ref<string>('')

function playTickSound () {
  if (tickSound.value) {
    tickSound.value.currentTime = 0 // Reset sound to start
    tickSound.value.play()
  }
}

function runRandomizer() {
  if (isSpinning.value) {
    return 
  }

  isSpinning.value = true

  const iterations = 20
  const finalSelection = Math.floor(Math.random() * props.items.length);

  let speed = 100
  let currentIteration = 0

  function animate () {
    // Animate the grid as long as the
    // iteration count is below "iterations"
    if (currentIteration < iterations) {
      // Ensures that we loop back to a square if the count goes
      // over the total number of available squares
      const currentIndex = currentIteration % props.items.length
      squareName.value = props.items[currentIndex].value

      playTickSound()

      // speed += currentIteration / 2 // Decreseases speed at the end
      speed += (currentIteration / 2) * (currentIteration > 15 ? 2 : 1) // Increases speed at the end
      currentIteration++
      setTimeout(animate, speed)
    } else {
      // Once the iteration is complete, show the final
      // selected result
      squareName.value = props.items[finalSelection].value;
      isSpinning.value = false;
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

onMounted(() => {
  tickSound.value = document.getElementById('tickSound') as HTMLAudioElement

  if (tickSound.value && !props.mute) {
    tickSound.value.volume = 0.3;
  }
})

defineExpose({
  runRandomizer
})
</script>

<style lang="scss" scoped>
.floor {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border: 5px rgba(0, 0, 0, 1) solid;

  .square {
    transition: all .14s ease-in-out;
    width: auto;
    height: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    border: 1px black solid;
    cursor: pointer;

    &.spinning {
      cursor: not-allowed;
    }

    &.highlight {
      color: white;
      background-color: #7d7db3;
    }

    &:hover {
      background-color: rgba(0, 0, 0, 0.15);
    }
  }
}
</style>
