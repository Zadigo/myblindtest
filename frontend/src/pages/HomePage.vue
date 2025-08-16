<template>
  <section class="w-5xl mx-auto px-10 my-20 relative">
    <VoltCard class="mt-10 mb-5 shadow-none">
      <template #content>
        <div class="flex justify-end">
          <VoltButton class="rounded-full">
            <RouterLink :to="{ name: 'teams' }" class="inline-flex gap-2 items-center">
              Manage teamsa
              <VueIcon icon="i-fa7-solid:arrow-right" />
            </RouterLink>
          </VoltButton>
        </div>
      </template>
    </VoltCard>

    <div class="grid grid-cols-2 gap-2">
      <GeneralSettings />
      <PointValues />
      <GameModes />
    </div>
  </section>
</template>

<script setup lang="ts">
useLoadAutocompleteData()
</script>

<style lang="scss">
#side-panel {
  #panel {
    position: sticky;
    top: 0;
    left: 0;
  }
}
</style>
