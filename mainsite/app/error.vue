<template>
  <section class="font-sans relative">
    <nuxt-layout>
      <section class="error-page my-20">
        <div class="mx-auto md:max-w-2xl">
          <volt-card>
            <template #content>
              <h1 class="font-5xl">{{ error?.statusCode }}</h1>
              <p class="font-2xl font-light">{{ error?.message }}</p>

              <nuxt-link-locale id="link-error" to="/" aria-label="Accueil" @click="handleError">
                {{ 'Accueil' }}
              </nuxt-link-locale>
            </template>
          </volt-card>

          <dev-only>
            <div class="text-wrap overflow-y-scroll pa-10 rounded-3xl bg-primary-500 mt-10">
              {{ error }}
            </div>
          </dev-only>
        </div>
      </section>
    </nuxt-layout>
  </section>
</template>

<script setup lang="ts">
const error = useError()

useHead({
  title: "La page n'existe pas"
})

/**
 * A function that handles the
 * redirect to the home page
 */
function handleError() {
  clearError({ redirect: '/' })
}
</script>
