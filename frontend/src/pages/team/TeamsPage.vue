<template>
  <section class="w-4xl mx-auto px-10 my-20 relative">
    <div class="grid grid-cols-12 gap-2 my-10">
      <div class="col-span-12">
        <volt-card>
          <template #content>
            <div class="space-x-2 flex justify-between">
              <volt-secondary-button rounded>
                <vue-icon icon="fa-solid:arrow-left" />
                <router-link :to="{ name: 'home' }">
                  Back to settings
                </router-link>
              </volt-secondary-button>

              <volt-secondary-button rounded>
                <router-link :to="{ name: 'blind_test', query: { id: sessionId } }" class="flex items-center gap-2">
                  Go to blindtest
                </router-link>
                <vue-icon icon="fa-solid:arrow-right" />
              </volt-secondary-button>
            </div>
          </template>
        </volt-card>
      </div>

      <!-- TODO: Simplify with one component -->
      <div class="col-span-6">
        <volt-card>
          <template #content>
            <volt-input-text v-if="teamOne" v-model="teamOne.name" class="w-full" placeholder="Team name" />
            <volt-skeleton v-else height="100px" />
          </template>
        </volt-card>
      </div>

      <div class="col-span-6">
        <volt-card>
          <template #content>
            <volt-input-text v-if="teamTwo" v-model="teamTwo.name" class="w-full" placeholder="Team name" />
            <volt-skeleton v-else height="100px" />
          </template>
        </volt-card>
      </div>

      <!-- <div class="col-span-12">
        <color-wheel />
      </div> -->
    </div>
  </section>
</template>

<script setup lang="ts">
/**
 * Session
 */
const { sessionId } = useSession()

/**
 * Teams
 */
const teamStore = useTeamsStore()
const { teamOne, teamTwo } = storeToRefs(teamStore)

/**
 * SEO
 */

useHead({
  title: 'Settings',
  meta: [
    {
      name: 'description',
      content: 'Configure your teams for the blind test game.',
    }
  ]
})
</script>
