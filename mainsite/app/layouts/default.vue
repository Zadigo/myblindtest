<template>
  <section ref="sectionEl" id="layout-site">
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

    <!-- Main -->
    <!-- <router-view v-slot="{ Component }">
      <Transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 -translate-x-10 blur-sm" enter-to-class="opacity-100 translate-x-0 blur-none" leave-active-class="duration-300 ease-in" leave-from-class="opacity-100 translate-x-0 blur-none" leave-to-class="opacity-0 translate-x-10 blur-sm" mode="out-in">
        <component :is="Component" />
      </Transition>
    </router-view> -->
    <slot />
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
