<template>
  <div class="absolute top-0 left-0 w-full h-auto bg-surface-50 dark:bg-surface-800 px-5 py-2 z-40 flex justify-between items-center">
    <div class="flex justify-left items-center gap-2">
      <volt-secondary-button>
        <vue-icon icon="lucide:home" />
        Home
      </volt-secondary-button>

      <volt-dropdown id="settings" :items="items">
        <template #default="{ attrs }">
          <volt-secondary-button @click="attrs.toggle">
            <vue-icon icon="lucide:cog" />
            Settings
          </volt-secondary-button>
        </template>
      </volt-dropdown>
    </div>

    <div class="flex gap-2">
      <volt-badge class="cursor-pointer text-sm" @click="() => copy()">
        <div class="flex gap-2">
          {{ sessionId }}
          <vue-icon icon="lucide:copy" />
        </div>
      </volt-badge>
  
      <volt-badge v-if="isConnected" class="animate-pulse gap-2">
        <vue-icon icon="lucide:circle" />
        Connected
      </volt-badge>

      <volt-badge v-else severity="danger" class="cursor-pointer gap-2">
        <vue-icon icon="lucide:circle-off" />
        Disconnected
      </volt-badge>
    </div>
  </div>
</template>

<script setup lang="ts">
const items = ref([
  {
    label: 'Options',
    items: [
      {
        label: 'Refresh'
      },
      {
        label: 'About'
      }
    ]
  }
])

/**
 * State
 */

const { isConnected } = useGameWebsocket()

/**
 * Session copy
 */

const { sessionId } = useSession()
const { copy } = useClipboard({ source: sessionId })
</script>
