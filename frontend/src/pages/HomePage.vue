<template>
  <section class="relative mx-auto my-3 w-full px-5 md:my-20 md:px-0 md:w-5xl">
    <volt-card id="second-header" class="mt-10 mb-5 shadow-none">
      <template #content>
        <div class="grid grid-cols-2">
          <volt-label id="dark-mode" label-for="dark-mode">
            <volt-secondary-button>
              <router-link :to="{ name: 'home', params: { locale: 'en-Us' } }">
                <vue-icon icon="circle-flags:us-um" />
              </router-link>
            </volt-secondary-button>

            <volt-secondary-button>
              <router-link :to="{ name: 'home', params: { locale: 'fr-FR' } }">
                <vue-icon icon="circle-flags:fr" />
              </router-link>
            </volt-secondary-button>

            <volt-toggle-switch id="dark-mode" v-model="isDark">
              <template #handle="{ checked }">
                <vue-icon :icon="checked ? 'fa6-solid:moon' : 'fa6-solid:sun'" class="text-lg" />
              </template>
            </volt-toggle-switch>
          </volt-label>

          <div id="actions" class="flex justify-end gap-2">
            <volt-secondary-button :disabled="!hasExistingSession" rounded @click="() => reset()">
              <vue-icon icon="fa7-solid:clock-rotate-left" />
              <span class="hidden md:block">
                {{ $t('Reset') }}
              </span>
            </volt-secondary-button>

            <volt-secondary-button rounded class="rounded-full">
              <router-link :to="{ name: 'blind_test', params: { id: sessionId } }" class="inline-flex gap-2 items-center">
                <span class="hidden md:block">
                  {{ $t('Start') }}
                </span>
                <vue-icon icon="fa7-solid:arrow-right" />
              </router-link>
            </volt-secondary-button>
          </div>
        </div>
      </template>
    </volt-card>

    <div id="blindtest-settings" class="grid grid-cols-1 items-center-safe md:grid-cols-2 md:items-start gap-2">
      <div class="space-y-2">
        <general-settings />
        <game-modes />
      </div>

      <div class="space-y-2">
        <point-values />
        <joker-settings />
      </div>
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
