<template>
  <section class="w-full md:w-5xl mx-auto my-20 relative">
    <volt-card class="mt-10 mb-5 shadow-none">
      <template #content>
        <volt-label label-for="dark-mode">
          <volt-toggle-switch id="dark-mode" v-model="isDark">
            <template #handle="{ checked }">
              <vue-icon :icon="checked ? 'fa6-solid:moon' : 'fa6-solid:sun'" class="text-lg" />
            </template>
          </volt-toggle-switch>
        </volt-label>

        <div class="flex justify-end gap-2">
          <volt-secondary-button :disabled="!hasExistingSession" rounded @click="() => reset()">
            <vue-icon icon="fa7-solid:clock-rotate-left" />
            Reset
          </volt-secondary-button>

          <volt-secondary-button rounded class="rounded-full">
            <router-link :to="{ name: 'blind_test', params: { id: sessionId } }" class="inline-flex gap-2 items-center">
              Start blindtest
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
const { reset, hasExistingSession, sessionId } = useSession()

/**
 * Dark mode
 */

const { isDark } = useDarkMode()

/**
 * SEO
 */

useHead({
  title: 'Blindtest challenge',
  meta: [
    {
      name: 'description',
      content:
        'Welcome to Volt Scorekeeper! Manage your sports scoring with ease using our intuitive platform designed for efficiency and accuracy.',
    },
  ],
})
</script>
