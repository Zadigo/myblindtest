<template>
  <div class="grid grid-cols-12 gap-3 text-center h-screen bg-primary-400 overflow-hidden transition-all duration-500 relative">
    <!-- Team 1 -->
    <team-block v-if="firstTeam" :team="firstTeam" position="left" :class="{ '-translate-x-100 duration-500 ease-in-out blur-sm': showAnswer, 'translate-x-0 duration-500 ease-in-out': !showAnswer }" class="col-span-6" />

    <!-- Team 2 -->
    <team-block v-if="secondTeam" :team="secondTeam" position="right" :class="{ 'translate-x-100 duration-500 ease-in-out blur-sm': showAnswer, 'translate-x-0 duration-500 ease-in-out': !showAnswer }" class="col-span-6" />

    <!-- Correct Answer -->
    <transition mode="in-out" enter-active-class="animated animate__zoomIn" leave-active-class="animated animate__zoomOut">
      <correct-answer v-if="showAnswer" />
    </transition>
  </div>
</template>

<script setup lang="ts">
import { useSound } from '@vueuse/sound'
import { collection, doc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'
import type { CacheSession, Team } from '@/types'

/**
 * Timer
 */

const { timerMinutes, timerSeconds } = useGameTimer()

/**
 * Consecutive answers
 */

const gameStore = useGameStore()
const { showAnswer, correctAnswerTeamId } = storeToRefs(gameStore)

/**
 * Session
 */

const { sessionId } = useSession()

const fireStore = useFirestore()

const defaultTeam: Team = {
  color: '#000000',
  name: 'Team',
  score: 0,
  id: 'default',
  players: [],
}

// const docRef = doc(collection(fireStore, 'blindtests'), sessionId.value)
let docRef: ReturnType<typeof doc> | undefined = undefined
let sessionData: ReturnType<typeof useDocument<CacheSession>> | undefined = undefined

if (isDefined(sessionId) && sessionId.value !== '') {
  docRef = doc(collection(fireStore, 'blindtests'), sessionId.value)
  sessionData = useDocument<CacheSession>(docRef)
}

const firstTeam = computed(() => {
  if (isDefined(sessionData) && isDefined(sessionData.value)) {
    return sessionData.value.teams[0]
  } else {
    return defaultTeam
  }
})
const secondTeam = computed(() => {
  if (isDefined(sessionData) && isDefined(sessionData.value)) {
    return sessionData.value.teams[1]
  } else {
    return defaultTeam
  }
})

/**
 * Sound effects
*/

const { play } = useSound('/win.mp3', { volume: 0.5 })

whenever(correctAnswerTeamId, () => { play() })
</script>
