<template>
  <volt-dialog v-model:visible="showConnectionUrl" title="Join the Game">
    <img :src="qrcode" alt="QR Code" />
    <p class="mt-4 text-center">Scan this QR code to join the game on your device!</p>
    {{ url }}
  </volt-dialog>
</template>

<script setup lang="ts">
import { useGlobalState } from '@/composables'
import { useQRCode } from '@vueuse/integrations/useQRCode'

const { showConnectionUrl } = useGlobalState()

/**
 * QR Code
 */

const { sessionId } = useSession()
const url = ref(`${import.meta.env.VITE_SITE_URL}/${sessionId.value}/single-player`)
const qrcode = useQRCode(url)
</script>
