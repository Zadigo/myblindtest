<template>
  <div ref="teamBlockEl" class="w-4/12 mx-auto">
    <div class="bg-primary-900 p-5 rounded-4xl text-surface-100 text-7xl font-bold text-center overflow-hidden cursor-pointer hover:shadow-xl hover:translate-y-2 transition-all ease-in-out">
      <!-- Score -->
      <div ref="scoreBoxEl">
        {{ teamScore }}
      </div>

      <!-- Team Name -->
      <p class="text-sm font-light">
        Team ({{ teamName }})
      </p>
    </div>

    <!-- Actions -->
    <new-team-actions :team="team" @animate="handleAnimations" />

    <!-- Consecutive Answers -->
    <transition class="animate__animated" enter-to-class="animate__zoomInLeft" leave-to-class="animate__fadeOutLeft">
      <h1 v-if="hasConsecutiveAnswers" class="text-5xl font-bold text-surface-700">
        Exceptionnel x {{ consecutiveAnswers }}
      </h1>
    </transition>

    <!-- Fireworks -->
    <base-fireworks v-show="gameStarted && hasConsecutiveAnswers" />
  </div>
</template>

<script setup lang="ts">

const { teamIndex = 1 } = defineProps<{ teamIndex: number }>()

/**
 * Game State
 */

const gameStarted = inject('gameStarted')

/**
 * Team
 */

const teamStore = useTeamsStore()
const team = teamStore.getTeamByIndex(teamIndex)

const teamName = computed(() => isDefined(team) ? team.value.name : (team.value?.id || 'Unknown Team'))
const teamScore = computed(() => isDefined(team) ? team.value.score : 0)

/**
 * Consecutive answers
 */

const { consecutiveAnswers, hasConsecutiveAnswers } = useConsecutiveAnswers(team, 2)

/**
 * Animations
 */

const { handleAnimation: handleTeamBlockAnimation } = useAnimationComposable('teamBlockEl')
const { handleAnimation: handleScoreAnimation } = useAnimationComposable('scoreBoxEl')

async function handleAnimations() {
  await handleTeamBlockAnimation()
  await handleScoreAnimation()
}
</script>
