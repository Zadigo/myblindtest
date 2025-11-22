<template>
  <volt-card ref="cardEl" class="h-40" @mouseenter="() => toggleIsHovered(true)" @mouseleave="() => toggleIsHovered(false)">
    <template #content>
      <div v-if="player" class="text-center flex-row justify-center items-center w-full">
        <div v-if="isHovered" class="space-y-2">
          <volt-button class="w-full" size="small" @click="() => sendCorrectAnswer(playerId, 'Artist')">
            <vue-icon icon="i-lucide:type" />
            Artist
          </volt-button>

          <volt-button class="w-full" size="small" @click="() => sendCorrectAnswer(playerId, 'Title')">
            <vue-icon icon="i-lucide:type" />
            Title
          </volt-button>

          <volt-button class="w-full" size="small" @click="() => sendCorrectAnswer(playerId, 'Both')">
            <vue-icon icon="i-lucide:type" />
            Both
          </volt-button>
        </div>

        <div v-else>
          <h2 class="font-bold text-5xl text-primary-100 rounded-xl p-2 dark:bg-primary-800 mb-4">
            {{ player.points }}
          </h2>

          <h5 class="font-bold mb-4 overflow-hidden text-ellipsis whitespace-nowrap text-primary-100">
            {{ player.name }}
          </h5>

        </div>
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
const props = defineProps<{ playerId: string }>()

const  cardEl = useTemplateRef('cardEl')
const isHovered = useElementHover(cardEl)

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
