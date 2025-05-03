<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        {{ gameUpdates }}

        <BlindTestLayout>
          <template #teamOne>
            <TeamBlock :team-id="0" :diffusion-mode="true" />
          </template>

          <template #teamTwo>
            <TeamBlock :team-id="1" :diffusion-mode="true" />
          </template>
        </BlindTestLayout>

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
import { getBaseUrl } from '@/plugins/client'
import { WebsocketDiffusionMessage } from '@/types'
import { useWebSocket } from '@vueuse/core'
import { computed, ref } from 'vue'
import { useWebsocketUtilities } from '@/composables/utils'
import { useSongs } from '@/stores/songs'

import BlindTestLayout from '@/layouts/BlindTestLayout.vue'
import TeamBlock from '@/components/blindtest/TeamBlock.vue'
import { defaults } from '@/data'
import { toast } from 'vue-sonner'

const songStore = useSongs()
const { parseMessage, sendMessage } = useWebsocketUtilities()

const deviceId = ref<string>()
const gameUpdates = ref<WebsocketDiffusionMessage[]>([])

const ws = useWebSocket(getBaseUrl('/ws/connect', null, true), {
  immediate: false,
  // heartbeat: {
  //   message: JSON.stringify({'message': 'ping'}),
  //   interval: 1000
  // },
  onMessage() {
    const data = parseMessage<WebsocketDiffusionMessage>(ws.data.value)

    console.log(data)

    switch (data.action) {
      case 'initiate_connection':
        deviceId.value = data.device_id
        toast.success('Device connected', {
          description: `Device ID is: ${data.device_id}`
        })
        break

      case 'game_disconnected':
        songStore.cache = defaults.cache
        ws.close()
        break

      case 'game_updates':
        songStore.cache.teams[data.updates.team_id].score = data.updates.points
        gameUpdates.value.push(data)
        break

      case 'apply_cache':
        console.log(data)
        songStore.cache = data.cache
        break

      default:
        break
    }
  }
})

const isConnected = computed(() => {
  return ws.status.value === 'OPEN'
})

function handleConnect() {
  ws.open()
  ws.send(sendMessage({
    action: 'update_device_cache',
    device_id: deviceId.value
  }))
}

function handleDisconnect() {
  ws.close()
}
</script>
