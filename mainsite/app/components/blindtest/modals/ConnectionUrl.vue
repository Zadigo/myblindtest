<template>
  <volt-dialog v-model:visible="showConnectionUrl" title="Join the Game" modal>
    <div class="flex-col place-items-center w-full text-center">
      <img :src="qrcode" alt="QR Code" />

      <div class="mt-5">
        <p class="mt-4 text-center">Scan this QR code to join the game on your device!</p>
        <div class="p-5 rounded-lg bg-secondary-100 dark:bg-secondary-800 text-center break-all mt-4 flex items-center justify-between">
          <span class="text-ellipsis block">{{ url }}</span>
          <volt-secondary-button size="small" @click="() => copy()">
            <icon name="lucide:copy" />
          </volt-secondary-button>
        </div>
      </div>
    </div>
  </volt-dialog>
</template>

<script setup lang="ts">
import { useQRCode } from '@vueuse/integrations/useQRCode'

/**
 * Modal
 */

const { showConnectionUrl } = useGlobalState()

/**
 * QR Code
 */

const { locale } = useI18n()
const { sessionId } = useSession()

const config = useRuntimeConfig()
const url = ref(`${config.public.siteUrl}/${locale.value}/blindtest/player?game=${sessionId?.value}`)

const qrcode = useQRCode(url, { size: 300 })

/**
 * Copy
 */

const { copy } = useClipboard({ source: url })
</script>
