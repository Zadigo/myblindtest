<template>
  <div ref="scoreEl" class="score">
    <h1 class="mb-0">15</h1>
    <p class="text-uppercase fw-light">Points</p>
  </div>
</template>

<script setup lang="ts">
// import { useAnimate, whenever } from '@vueuse/core';
import { ref, watch } from 'vue';

const scoreEl = ref<HTMLElement>()
// const { play } = useAnimate(scoreEl, { transform: 'rotate(10deg)' }, 1000)

const props = defineProps({
  animateScore: {
    type: Boolean,
    default: false
  }
})

watch(() => props.animateScore, (newValue) => {
  if (scoreEl.value) {
    if (newValue) {
        scoreEl.value.classList.remove('animate__animated', 'animate__bounce')
      scoreEl.value.classList.add('animate__animated', 'animate__bounce')
    } else {
      scoreEl.value.classList.remove('animate__animated', 'animate__bounce')
    }
  }
})
</script>

<style lang="scss">
.score {
  color: white;
  background-color: #111;
  padding: 1rem;
  border-radius: 20px;
  text-align: center;
}
</style>
