<template>
  <div class="absolute top-0 left-0 w-full h-auto bg-surface-300/70 dark:bg-surface-800 px-5 py-2 z-50 flex justify-between items-center">
    <div class="flex justify-left items-center gap-2">
      <router-link :to="{ name: 'home' }">
        <volt-secondary-button>
          <vue-icon icon="lucide:home" />
          {{ $t('Home') }}
        </volt-secondary-button>
      </router-link>

      <volt-dropdown id="settings" :items="items">
        <template #default="{ attrs }">
          <volt-secondary-button @click="attrs.toggle">
            <vue-icon icon="lucide:cog" />
            {{ $t('Settings') }}
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
        {{ $t('Connected') }}
      </volt-badge>

      <volt-badge v-else severity="danger" class="cursor-pointer gap-2" @click="wsObject.open()">
        <vue-icon icon="lucide:circle-off" />
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
        label: t('About')
      }
    ]
  }
])

/**
 * State
 */

const { isConnected, wsObject } = useAdminWebsocket()

/**
 * Session copy
 */

const { sessionId } = useSession()
const { copy } = useClipboard({ source: sessionId })
</script>
