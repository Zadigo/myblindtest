<template>
  <div class="space-y-2">
    <sound-effect id="sound-title" name="camera">
      <template #default="{ attrs }">
        <volt-secondary-button class="w-full" size="small" @click="attrs.playSound(() => sendCorrectAnswer(playerId, 'Artist'))">
          <icon name="lucide:star-half" />
          Artist
        </volt-secondary-button>
      </template>
    </sound-effect>

    <sound-effect id="sound-title" name="camera">
      <template #default="{ attrs }">
        <volt-secondary-button class="w-full" size="small" @click="attrs.playSound(() => sendCorrectAnswer(playerId, 'Title'))">
          <icon name="lucide:star-half" />
          Title
        </volt-secondary-button>
      </template>
    </sound-effect>

    <sound-effect id="sound-title" name="camera">
      <template #default="{ attrs }">
        <volt-secondary-button class="w-full" size="small" @click="attrs.playSound(() => sendCorrectAnswer(playerId, 'Both'))">
          <icon name="lucide:star" />
          Both
        </volt-secondary-button>
      </template>
    </sound-effect>

    <reconnect-button :player-id="playerId" />
  </div>

</template>

<script setup lang="ts">
defineProps<{ playerId: string }>()

/**
 * Actions
 */

const { wsObject, gameStarted } = useAdminWebsocket()
const { sendCorrectAnswer } = useGameActions(wsObject, gameStarted)
</script>
