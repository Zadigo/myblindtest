<template>
  <section id="interface" class="mx-5">
    <div class="px-5">
      <game-block v-if="canDiffuse" />
      <connection-block v-else @check-code="(code) => checkPinCode(code)" />
    </div>

    <!-- Modals -->
    <volt-dialog v-model:visible="showAnswer" :modal="true" class="w-[400px]">
      <div class="text-center">
        <h1 class="font-bold text-3xl mb-1">
          Mariah Carey
        </h1>
        <p class="font-light text-2xl">
          We belong together
        </p>
      </div>
    </volt-dialog>

    <!-- Audio -->
    <audio ref="audioEl">
      <source src="/win.mp3" type="audio/mpeg">
    </audio>
  </section>
</template>

<script setup lang="ts">
import 'animate.css'

import { useGameWebsocket } from '@/composables'

const { connect, checkPinCode, showAnswer } = useGameWebsocket()

const connectionStore = useConnectionStore()
const { canDiffuse } = storeToRefs(connectionStore)

onMounted(() => {
  connect()
  document.body.classList.add('h-screen', 'bg-no-repeat', 'bg-gradient-to-b', 'from-primary-100', 'to-primary-50')
})

onUnmounted(() => {
  document.body.classList.remove('h-screen', 'bg-no-repeat', 'bg-gradient-to-b', 'from-primary-100', 'to-primary-50')
})
</script>
