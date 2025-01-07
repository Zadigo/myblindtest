<template>
  <div class="row">
    <div class="col-8">
      <div class="card">
        <div class="card-body">
          <div class="floor" @click="runRandomizer">
            <div v-for="detail in wheelDetaults" :key="detail.id" :class="{highlight: detail.value === squareName}" class="square">
              <span>{{ detail.value }}</span>
            </div>
          </div>
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
import { wheelDetaults } from '@/data/defaults';
import { onMounted, ref } from 'vue';

const emit = defineEmits({
  completed (_value: string) {
    return true
  }
})

// Audio elements
const tickSound = ref<HTMLAudioElement | null>(null);

const isSpinning = ref(false)
const squareName = ref<string>('')

function playTickSound () {
  if (tickSound.value) {
    tickSound.value.currentTime = 0; // Reset sound to start
    tickSound.value.play();
  }
}

function runRandomizer() {
  if (isSpinning.value) {
    return 
  }

  isSpinning.value = true

  const iterations = 20
  let speed = 100
  let currentIteration = 0

  const finalSelection = Math.floor(Math.random() * wheelDetaults.length);

  function animate () {
    if (currentIteration < iterations) {
      const currentIndex = currentIteration % wheelDetaults.length
      squareName.value = wheelDetaults[currentIndex].value

      playTickSound()

      speed += currentIteration / 2
      currentIteration++
      setTimeout(animate, speed);
    } else {
      squareName.value = wheelDetaults[finalSelection].value;
      isSpinning.value = false;
    }
  }

  animate()
  emit('completed', squareName.value)
}

onMounted(() => {
  tickSound.value = document.getElementById('tickSound') as HTMLAudioElement

  if (tickSound.value) {
    tickSound.value.volume = 0.3;
  }
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
    height: 100px;
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
