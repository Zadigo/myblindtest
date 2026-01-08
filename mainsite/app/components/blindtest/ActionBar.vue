<template>
  <div class="absolute top-0 left-0 w-full h-auto bg-surface-300/70 dark:bg-surface-800 px-5 py-2 z-50 flex justify-between items-center">
    <div class="flex justify-left items-center gap-2">
      <nuxt-link-locale to="/">
        <volt-secondary-button>
          <icon name="lucide:home" />
          {{ $t('Home') }}
        </volt-secondary-button>
      </nuxt-link-locale>

      <volt-dropdown id="settings" :items="items">
        <template #default="{ attrs }">
          <volt-secondary-button @click="attrs.toggle">
            <icon name="lucide:cog" />
            {{ $t('Settings') }}
          </volt-secondary-button>
        </template>
      </volt-dropdown>
    </div>

    <div class="flex gap-2">
      <volt-badge class="cursor-pointer text-sm" @click="() => copy()">
        <div class="flex gap-2">
          {{ sessionId }}
          <icon name="lucide:copy" />
        </div>
      </volt-badge>

      <volt-badge v-if="isConnected" class="animate-pulse gap-2">
        <icon name="lucide:circle" />
        {{ $t('Connected') }}
      </volt-badge>

      <volt-badge v-else severity="danger" class="cursor-pointer gap-2" @click="wsObject.open()">
        <icon name="lucide:circle-off" />
        {{ $t('Disconnected') }}
      </volt-badge>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useGlobalState } from '@/composables'
import type { MenuItem } from 'primevue/menuitem'

/**
 * Devices
 */

const devicesStore = useDevicesStore()
const { showDevicesModal } = storeToRefs(devicesStore)

/**
 * Connection Url
 */

const { toggleShowConnectionUrl } = useGlobalState()

/**
 * State
 */

const { isConnected, wsObject, gameStarted } = useAdminWebsocket()
const { stopGame } = useGameActions(wsObject, gameStarted)

/**
 * Dark mode
 */

const { isDark, toggleDark } = useDarkMode()
const { t } = useI18n()

const items: MenuItem = ref([
  {
    label: t('Options'),
    items: [
      {
        label: t('Devices'),
        command() {
          showDevicesModal.value = true
        }
      },
      {
        label: t('Connection url'),
        command: () => toggleShowConnectionUrl(true)
      },
      {
        label: computed(() => isDark.value ? t('Light mode') : t('Dark mode')),
        icon: isDark.value ? 'fa7-solid:sun' : 'fa7-solid:moon',
        command: () => toggleDark()
      },
      {
        label: t('Stop game'),
        command: () => stopGame()
      },
      {
        label: t('About')
      }
    ]
  }
])

/**
 * Session copy
 */

const { sessionId } = useSession()
const { copy } = useClipboard({ source: sessionId })
</script>
