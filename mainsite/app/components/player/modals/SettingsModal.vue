<template>
  <volt-dialog v-model:visible="show" modal>
    <template #header>
      <h2 class="text-2xl font-bold">
        {{ $t("Settings") }}
      </h2>
    </template>

    <form v-if="player">
      <volt-fluid class="space-y-2">
        <volt-input-text v-model="playerName" :placeholder="$t('Name')" />
        <volt-input-text v-model="genreSpeciality" :disabled="true" :placeholder="$t('Genre speciality')" />
      </volt-fluid>
    </form>

    <template #footer>
      <volt-button @click="() => toggleSettingsModal()">
        {{ $t("Close") }}
      </volt-button>
    </template>
  </volt-dialog>
</template>

<script setup lang="ts">
import type { BlindtestPlayer, Undefineable } from '~/types'
import { doc, updateDoc } from 'firebase/firestore'
import { useFirestore } from 'vuefire'

const props = defineProps<{ player: Undefineable<BlindtestPlayer> }>()

const show = defineModel('show', { type: Boolean, required: true })
const toggleSettingsModal = useToggle(show)

/**
 * Websocket
 */

const { wsObject } = usePlayerWebsocket()

/**
 * Fields
 */

const firestore = useFirestore()
const route = useRoute()

const { stringify } = useWebsocketMessage()

const playerName = ref<string>('')
const genreSpeciality = ref<string>('')

const { history } = useRefHistory(playerName)


watchDebounced(playerName, async (newName) => {
  const docRef = doc(firestore, 'blindtests', route.params.id as string)
  
  await updateDoc(docRef, { [`players.${props.player?.id}.name`]: newName })
  wsObject.send(stringify({ action: 'update_player', id: props.player?.id, name: newName }))
}, {
  debounce: 2000
})
</script>
