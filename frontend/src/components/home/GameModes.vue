<template>
  <VoltCard class="border-0 bg-brand-shade-3/30 shadow-none">
    <template #title>
      <h3 class="font-bold">
        Game modes
      </h3>
    </template>

    <template v-if="currentSettings" #content>
      <div class="py-3">
        <volt-label>
          <volt-switch v-model="currentSettings.settings.soloMode" />
          <label>Run in solo mode</label>
        </volt-label>
      </div>

      <div class="py-3">
        <volt-label>
          <volt-switch v-model="currentSettings.settings.adminPlays" />
          <label>Admin is registered in a team</label>
        </volt-label>
      </div>
    </template>

    <template v-else #content>
      <volt-skeleton class="h-96" />
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
const { currentSettings } = useGlobalSessionState()
</script>
