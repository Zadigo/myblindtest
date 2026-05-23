<template>
  <volt-button size="small" @click="() => reconnectPlayer(playerId)">
    <icon name="lucide:refresh-cw" class="mr-2" />
    Reconnect
  </volt-button>
</template>

<script setup lang="ts">
defineProps<{ playerId: string }>()

/**
 * Actions
 */

const { wsObject, gameStarted } = useAdminWebsocket()
const { reconnectPlayer } = useGameActions(wsObject, gameStarted)
</script>
