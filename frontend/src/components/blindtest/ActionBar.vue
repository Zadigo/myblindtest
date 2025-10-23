<template>
  <div class="absolute top-0 left-0 w-full h-auto bg-surface-50 dark:bg-surface-800 px-5 py-2 z-40 flex justify-between items-center">
    <div class="flex justify-left items-center">
      <volt-secondary-button size="small">
        <vue-icon icon="lucide:home" />
      </volt-secondary-button>

      <volt-dropdown id="settings" :items="items">
        <template #default="{ attrs }">
          <volt-secondary-button size="small" @click="attrs.toggle">
            <vue-icon icon="lucide:cog" />
            Settings
          </volt-secondary-button>
        </template>
      </volt-dropdown>
    </div>

    <volt-badge size="small" class="animate-pulse gap-2">
      <vue-icon icon="lucide:circle" />
      Connected
    </volt-badge>
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
</script>
