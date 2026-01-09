<template>
  <section id="layout-site" ref="sectionEl">
    <!-- Navbar -->
    <header class="hidden md:flex">
      <base-navbar>
        <base-navbar-content>
          <template #brand>
            <nuxt-link-locale to="/">
              Blindtest
            </nuxt-link-locale>
          </template>

          <base-navbar-links>
            <base-navbar-link>
              <nuxt-link-locale to="/">
                {{ $t('Home') }}
              </nuxt-link-locale>
            </base-navbar-link>

            <base-navbar-link>
              <nuxt-link-locale to="/create-songs">
                {{ $t('Songs') }}
              </nuxt-link-locale>
            </base-navbar-link>

            <base-navbar-link>
              <nuxt-link-locale to="/statistics">
                {{ $t('Statistics') }}
              </nuxt-link-locale>
            </base-navbar-link>

            <base-navbar-link>
              <nuxt-link-locale to="/about">
                {{ $t('About') }}
              </nuxt-link-locale>
            </base-navbar-link>
          </base-navbar-links>
        </base-navbar-content>
      </base-navbar>
    </header>

    <slot />

    <!-- <base-footer /> -->
  </section>
</template>

<script setup lang="ts">
// import { onBeforeRouteLeave, useRoute } from 'vue-router'

// const meta = useRoute().meta as { heightScreen: boolean }
// const sectionEl = useTemplateRef('sectionEl')

// onBeforeRouteLeave(() => {
//   if (meta.heightScreen) {
//     sectionEl.value?.classList.add('h-screen')
//   } else {
//     sectionEl.value?.classList.remove('h-auto')
//   }
// })
</script>
