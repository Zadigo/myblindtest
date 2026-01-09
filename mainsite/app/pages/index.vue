<template>
  <section class="relative mx-auto my-3 w-full px-5 md:my-20 md:px-0 md:w-5xl">
    <volt-card id="second-header" class="mt-10 mb-5 shadow-none">
      <template #content>
        <div class="grid grid-cols-2">
          <div class="inline-flex gap-2">
            <volt-secondary-button aria-label="Switch to enlish">
              <nuxt-link-locale to="/" locale="en">
                <icon name="circle-flags:us-um" />
              </nuxt-link-locale>
            </volt-secondary-button>
            
            <volt-secondary-button aria-label="Switch to french">
              <nuxt-link-locale to="/" locale="fr">
                <icon name="circle-flags:fr" />
              </nuxt-link-locale>
            </volt-secondary-button>
            
            <volt-label id="dark-mode" label-for="dark-mode">
              <volt-toggle-switch id="dark-mode" v-model="isDark">
                <template #handle="{ checked }">
                  <icon :name="checked ? 'fa6-solid:moon' : 'fa6-solid:sun'" class="text-lg" />
                </template>
              </volt-toggle-switch>
            </volt-label>
          </div>

          <div id="actions" class="flex justify-end gap-2">
            <volt-secondary-button :disabled="!hasExistingSession" rounded @click="() => reset()">
              <icon name="fa7-solid:clock-rotate-left" />
              <span class="hidden md:block">
                {{ $t('Reset') }}
              </span>
            </volt-secondary-button>

            <volt-secondary-button rounded class="rounded-full">
              <nuxt-link-locale :to="`/blindtest?id=${sessionId}`" class="inline-flex gap-2 items-center">
                <span class="hidden md:block">
                  {{ $t('Start') }}
                </span>
                <icon name="fa7-solid:arrow-right" />
              </nuxt-link-locale>
            </volt-secondary-button>
          </div>
        </div>
      </template>
    </volt-card>

    <div id="blindtest-settings" class="grid grid-cols-1 items-center-safe md:grid-cols-2 md:items-start gap-2">
      <div class="space-y-2">
        <home-general-settings />
        <home-game-modes />
      </div>

      <div class="space-y-2">
        <home-point-values />
        <home-joker-settings />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
/**
 * Session
 */
const { sessionId, hasExistingSession, reset } = useSession()

/**
 * Dark mode
 */

const { isDark } = useDarkMode()

/**
 * SEO
 */

const { locale } = useI18n()

const titles = {
  en: 'Blindtest challenge',
  fr: 'Défi Blindtest',
}

const descriptions = {
  'en': 'Join the ultimate blindtest challenge! Test your music knowledge with friends and climb the leaderboard. Are you ready to take on the challenge?',
  'fr': "Rejoignez le défi blindtest ultime ! Testez vos connaissances musicales avec des amis et grimpez dans le classement. Êtes-vous prêt à relever le défi ?",
}

useHead({
  title: titles[locale.value],
  meta: [
    {
      name: 'description',
      content: descriptions[locale.value],
    },
  ],
})
</script>
