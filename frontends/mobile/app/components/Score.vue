<template>
  <div ref="scoreEl" class="rounded-xl bg-black text-white text-center p-4 animate__animated animate__bounce">
    <h1 class="text-5xl mb-0">15</h1>
    <p class="text-uppercase font-light">
      Points
    </p>
  </div>
</template>

<script setup lang="ts">

const scoreEl = ref<HTMLElement>()

const props = defineProps<{ animateScore: boolean }>()

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
