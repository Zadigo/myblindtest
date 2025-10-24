<template>
  <div :id="id">
    <slot :attrs="{ playSound }" />
  </div>
</template>

<script setup lang="ts">
import { useSound } from '@vueuse/sound'

const props = defineProps<{ id: string, name: string }>()
const { play } = useSound(`${props.name}.mp3`, { volume: 0.5 })

function playSound(callback?: () => void) {
  play()
  
  if (callback) {
    callback()
  }
}
</script>
