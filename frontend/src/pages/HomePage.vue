<template>
  <section class="w-full md:w-5xl mx-auto my-20 relative">
    <volt-card class="mt-10 mb-5 shadow-none">
      <template #content>
        <div class="flex justify-end gap-2">
          <volt-secondary-button :disabled="!hasExistingSession" rounded @click="() => reset()">
            <vue-icon icon="fa7-solid:clock-rotate-left" />
            Reset
          </volt-secondary-button>

          <volt-secondary-button rounded class="rounded-full">
            <router-link :to="{ name: 'teams' }" class="inline-flex gap-2 items-center">
              Manage teams
              <vue-icon icon="fa7-solid:arrow-right" />
            </router-link>
          </volt-secondary-button>
        </div>
      </template>
    </volt-card>

    <div class="grid grid-rows-2 md:grid-cols-2 gap-2">
      <general-settings />
      <point-values />
      <game-modes />
    </div>
  </section>
</template>

<script setup lang="ts">
/**
 * Initiate session
 */
const { reset, hasExistingSession } = useSessionManager()

/**
 * SEO
 */

useHead({
  title: 'Home',
  meta: [
    {
      name: 'description',
      content:
        'Welcome to Volt Scorekeeper! Manage your sports scoring with ease using our intuitive platform designed for efficiency and accuracy.',
    },
  ],
})
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
