<template>
  <section ref="sectionEl" id="layout-site">
    <!-- Navbar -->
    <header class="hidden md:flex">
      <navbar>
        <navbar-content>
          <template #brand>
            <router-link :to="{ name: 'home' }">
              Blindtest
            </router-link>
          </template>

          <navbar-links>
            <navbar-link>
              <router-link :to="{ name: 'home' }">
                {{ $t('Home') }}
              </router-link>
            </navbar-link>

            <navbar-link>
              <router-link :to="{ name: 'create' }">
                {{ $t('Songs') }}
              </router-link>
            </navbar-link>

            <navbar-link>
              <router-link :to="{ name: 'statistics' }">
                {{ $t('Statistics') }}
              </router-link>
            </navbar-link>

            <navbar-link>
              <router-link :to="{ name: 'about' }">
                {{ $t('About') }}
              </router-link>
            </navbar-link>
          </navbar-links>
        </navbar-content>
      </navbar>
    </header>

    <!-- Main -->
    <router-view v-slot="{ Component }">
      <Transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 -translate-x-10 blur-sm" enter-to-class="opacity-100 translate-x-0 blur-none" leave-active-class="duration-300 ease-in" leave-from-class="opacity-100 translate-x-0 blur-none" leave-to-class="opacity-0 translate-x-10 blur-sm" mode="out-in">
        <component :is="Component" />
      </Transition>
    </router-view>
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
