<template>
  <div class="grid grid-cols-12 gap-3 text-center my-20">
    <!-- Team 1 -->
    <team-block v-if="firstTeam" ref="teamOneEl" :team="firstTeam" :correct-answer="correctAnswer" class="col-span-5" />

    <!-- Timer -->
    <div class="grid grid-flow-col grid-rows-3 gap-1 col-span-2">
      <div id="timer" class="shadow-none bg-primary-900 rounded-md flex justify-center place-items-center row-start-1">
        <span class="font-semibold text-3xl text-primary-50 block text-center">
          {{ timerMinutes }}:{{ timerSeconds }}
        </span>
      </div>
    </div>

    <!-- Team 2 -->
    <team-block v-if="secondTeam" ref="teamTwoEl" :team="secondTeam" :correct-answer="correctAnswer" class="col-span-5" />
  </div>
</template>

<script setup lang="ts">
import { CacheSession } from '@/types'
import { collection, doc } from 'firebase/firestore'
import { useFirestore, useDocument } from 'vuefire'

const teamOneEl = useTemplateRef('teamOneEl')
const teamTwoEl = useTemplateRef('teamTwoEl')

const { timerMinutes, timerSeconds } = useGameTimer()

const correctAnswer = ref<number>(0)

const connectionStore = useConnectionStore()
const { code } = storeToRefs(connectionStore)

code.value = 'hqqQ3UpvBWAEGWE0Jeoa'

const fireStore = useFirestore()
const docRef = doc(collection(fireStore, 'blindtests'), code.value)
const sessionData = useDocument<CacheSession>(docRef)

const firstTeam = computed(() => sessionData.value?.teams[0])
const secondTeam = computed(() => sessionData.value?.teams[1])
</script>
