<template>
  <div ref="cardEl" class="relative drop-shadow-xl w-48 h-64 overflow-hidden rounded-xl dark:bg-primary-100" @mouseenter="() => toggleIsHovered(true)" @mouseleave="() => toggleIsHovered(false)">
    <div class="absolute flex items-center justify-center dark:text-primary-50 z-1 opacity-90 rounded-xl inset-0.5 dark:bg-primary-900">
      <transition mode="out-in"  enter-active-class="animate__animated" leave-active-class="animate__animated" enter-to-class="animate__zoomIn" leave-from-class="animate__zoomOut">
        <div v-if="isHovered">
          <volt-fluid>
            <div class="space-y-4 max-w-[120px]">
              <volt-button @click="() => sendCorrectAnswer(playerId, 'Artist')">
                <vue-icon name="i-lucide:home" />
                Title
              </volt-button>

              <volt-button @click="() => sendCorrectAnswer(playerId, 'Artist')">
                <vue-icon icon="i-lucide:song-note" />
                Artist
              </volt-button>

              <volt-button @click="() => sendCorrectAnswer(playerId, 'Both')">
                <vue-icon icon="i-lucide:play-circle" />
                Both
              </volt-button>
            </div>
          </volt-fluid>
        </div>

        <div v-else class="flex-col content-center text-center space-y-4">
          <div class="font-bold text-7xl dark:text-primary-100 p-5 dark:bg-primary-800 rounded-xl">
            {{ player.points }}

            <p class="text-sm">
              Points
            </p>
          </div>


          <div class="text-ellipsis overflow-hidden max-w-[100px] mx-auto p-4 rounded-xl dark:bg-primary-800">
            {{ player.name }}
          </div>
        </div>
      </transition>
    </div>
    <div class="absolute w-56 h-48 dark:bg-primary-100 blur-[50px] -left-1/2 -top-1/2"></div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ playerId: string }>()

const cardEl = useTemplateRef('cardEl')

const [isHovered, toggleIsHovered] = useToggle(false)


/**
 * Player
 */

const { currentSettings } = useSession()

const player = computed(() => currentSettings.value?.players[props.playerId] || 0)

/**
 * Actions
 */

const { wsObject, gameStarted } = useGameWebsocketIndividual()
const { sendCorrectAnswer } = useGameActions(wsObject, gameStarted)
</script>
