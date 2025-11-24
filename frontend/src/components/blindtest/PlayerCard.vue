<template>
  <volt-card class="h-auto min-h-[197px]">
    <template #content>
      <div v-if="player" ref="cardEl" class="text-center flex-row justify-center items-center w-full">
        <div v-if="isHovered" class="space-y-2">
          <sound-effect id="sound-title" name="camera">
            <template #default="{ attrs }">
              <volt-secondary-button class="w-full" size="small" @click="attrs.playSound(() => sendCorrectAnswer(playerId, 'Artist'))">
                <vue-icon icon="lucide:star-half" />
                Artist
              </volt-secondary-button>
            </template>
          </sound-effect>

          <sound-effect id="sound-title" name="camera">
            <template #default="{ attrs }">
              <volt-secondary-button class="w-full" size="small" @click="attrs.playSound(() => sendCorrectAnswer(playerId, 'Title'))">
                <vue-icon icon="lucide:star-half" />
                Title
              </volt-secondary-button>
            </template>
          </sound-effect>

          <sound-effect id="sound-title" name="camera">
            <template #default="{ attrs }">
              <volt-secondary-button class="w-full" size="small" @click="attrs.playSound(() => sendCorrectAnswer(playerId, 'Both'))">
                <vue-icon icon="lucide:star" />
                Both
              </volt-secondary-button>
            </template>
          </sound-effect>
        </div>

        <div v-else>
          <div class="font-bold text-5xl text-primary-100 rounded-xl p-2 dark:bg-primary-800">
            {{ player.points }}
            <p class="text-sm">Points</p>
          </div>
          
          <!-- Consecutive Answers -->
          <div id="consecutive-answers" class="my-2 flex gap-1 justify-center items-center">
            <div v-for="i in 5" :key="i" :class="{ 'bg-secondary-50': i > consecutiveAnswers, 'bg-secondary-500': i <= consecutiveAnswers }" class="bg-secondary-100 h-3 w-3 rounded-sm" />
          </div>

          <h5 class="p-2 bg-primary-100 dark:bg-primary-800 rounded-xl font-bold mb-4 overflow-hidden text-ellipsis whitespace-nowrap text-primary-200 dark:text-primary-50">
            {{ player.name }}
          </h5>
        </div>
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
const props = defineProps<{ playerId: string }>()

const cardEl = useTemplateRef('cardEl')
const isHovered = useElementHover(cardEl)

/**
 * Player
 */

const { currentSettings } = useSession()

const player = computed(() => currentSettings.value?.players[props.playerId])

/**
 * Consecutive Answers
 */

const { consecutiveAnswers } = useConsecutiveAnswers(player)

/**
 * Actions
 */

const { wsObject, gameStarted } = useGameWebsocketIndividual()
const { sendCorrectAnswer } = useGameActions(wsObject, gameStarted)
</script>
