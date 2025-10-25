<template>
  <VoltCard class="border-0 bg-brand-shade-3/30">
    <template #title>
      <h3 class="font-bold">
        Game modes
      </h3>
    </template>

    <template v-if="currentSettings" #content>
      <div class="py-3">
        <volt-label label-for="solo-mode" label="Run in solo mode">
          <volt-toggle-switch v-model="currentSettings.settings.soloMode" />
        </volt-label>
      </div>

      <div class="py-3">
        <volt-label label-for="admin-plays" label="Admin is registered in a team">
          <volt-toggle-switch v-model="currentSettings.settings.adminPlays" />
        </volt-label>
      </div>
    </template>

    <template v-else #content>
      <volt-skeleton class="h-96" />
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
const { currentSettings } = useSession()
</script>
