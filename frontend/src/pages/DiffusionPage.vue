<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        {{ gameUpdates }}

        <v-btn v-if="isConnected" @click="handleDisconnect">
          Disconnect
        </v-btn>
        
        <v-btn v-else @click="handleConnect">
          Connect
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { getBaseUrl } from '@/plugins/client';
import { WebsocketDiffusionMessage } from '@/types';
import { useWebSocket } from '@vueuse/core';
import { computed, ref } from 'vue';

const gameUpdates = ref<WebsocketDiffusionMessage | null>()

const ws = useWebSocket(getBaseUrl('/ws/connect', null, true), {
  immediate: false,
  // heartbeat: {
  //   message: JSON.stringify({'message': 'ping'}),
  //   interval: 1000
  // },
  onMessage() {
    const data = JSON.parse(ws.data.value) as WebsocketDiffusionMessage

    switch (data.action) {
      case 'game_disconnected':
        break

      case 'game_updates':
        break

      case 'initiate_connection':
        break
    
      default:
        break;
    }

    gameUpdates.value = data
    console.log(data)
  }
})

const isConnected = computed(() => {
  return ws.status.value === 'OPEN'
})

function handleConnect() {
  ws.open()
}

function handleDisconnect() {
  ws.close()
  gameUpdates.value = null
}
</script>
