<template>
  <section id="interface" class="relative">
    <div class="px-10 flex justify-center items-center">
      <!-- Screen -->
      <game-block v-if="canDiffuse" />
      <!-- Connection -->
      <connection-block v-else @check-code="(code) => checkPinCode(code)" />
    </div>
    
    <!-- Answer -->
    <Transition enter-active-class="transition-all ease-in-out duration-300" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition-all ease-in-out duration-300" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
      <div v-if="showAnswer" class="absolute top-0 left-0 h-screen w-full bg-primary-800/80">
        <div class="p-20">
          <div v-if="answer" class="p-10 rounded-lg text-center my-30">
            <div class="rounded-full overflow-hidden w-60 h-60 mx-auto mb-10 shadow-sm animate transition-all animate-scalein duration-1000">
              <img :src="answer.artist.spotify_avatar" />
            </div>
            
            <h1 class="text-8xl font-bold text-primary-100">{{ answer.artist.name }}</h1>
            <p class="text-3xl font-light text-primary-100">{{ answer.name }}</p>

            <div id="stars" class="flex justify-center gap-2 mt-10">
              <vue-icon v-for="i in 5" icon="fa-solid:star" :class="i <= answer.difficulty ? 'text-primary-300' : 'text-primary-50'" class="text-3xl" />  
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- <div class="absolute top-0 left-0 w-full h-screen overflow-hidden has-[#screen]:opacity-70">
      <div id="screen" class="absolute top-0 left-0 w-full h-screen bg-primary-900 bg-gradient-to-tl from-primary-800 to-primary-500 opacity-70" />
      <img src="/screen_saver/img1.jpg" class="w-full h-full aspect-square object-cover" />
    </div> -->

    <!-- Audio -->
    <audio ref="audioEl">
      <source src="/win.mp3" type="audio/mpeg">
    </audio>
  </section>
</template>

<script setup lang="ts">
import 'animate.css'

import { useGameWebsocket } from '@/composables'

const { connect, checkPinCode } = useGameWebsocket()

const connectionStore = useConnectionStore()
const { canDiffuse, showAnswer, answer } = storeToRefs(connectionStore)

provide('showAnswer', showAnswer)
provide('answer', answer)

const audioEl = useTemplateRef<HTMLAudioElement>('audioEl')

whenever(showAnswer, () => {
  if (audioEl.value) {
    audioEl.value.play()
  }
})

onMounted(() => {
  document.body.classList.add('h-screen', 'bg-no-repeat', 'bg-gradient-to-b', 'from-primary-100', 'to-primary-50')
  connect()
})

onUnmounted(() => {
  document.body.classList.remove('h-screen', 'bg-no-repeat', 'bg-gradient-to-b', 'from-primary-100', 'to-primary-50')
})
</script>
