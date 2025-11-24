<template>
  <section ref="sectionEl" id="layout-site">
    <!-- Navbar -->
    <navbar class="hidden md:visible">
      <navbar-content>
        <template #brand>
          <router-link :to="{ name: 'home' }">
            Blindtest
          </router-link>
        </template>

        <navbar-links>
          <navbar-link>
            <router-link :to="{ name: 'home' }">
              Home
            </router-link>
          </navbar-link>

          <navbar-link>
            <router-link :to="{ name: 'create' }">
              Create
            </router-link>
          </navbar-link>

          <navbar-link>
            <router-link :to="{ name: 'statistics' }">
              Statistics
            </router-link>
          </navbar-link>

          <navbar-link>
            <router-link :to="{ name: 'about' }">
              About
            </router-link>
          </navbar-link>
        </navbar-links>
      </navbar-content>
    </navbar>

    <!-- Main -->
    <router-view v-slot="{ Component }">
      <Transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 -translate-x-10 blur-sm" enter-to-class="opacity-100 translate-x-0 blur-none" leave-active-class="duration-300 ease-in" leave-from-class="opacity-100 translate-x-0 blur-none" leave-to-class="opacity-0 translate-x-10 blur-sm" mode="out-in">
        <component :is="Component" />
      </Transition>
    </router-view>
  </section>
</template>

<script setup lang="ts">
import { onBeforeRouteLeave, useRoute } from 'vue-router'

const meta = useRoute().meta as { heightScreen: boolean }
const sectionEl = useTemplateRef('sectionEl')

onBeforeRouteLeave(() => {
  if (meta.heightScreen) {
    sectionEl.value?.classList.add('h-screen')
  } else {
    sectionEl.value?.classList.remove('h-auto')
  }
})

/**
 * Theme
 */

const bgTheme = ['dark:bg-primary-950', 'bg-no-repeat', 'bg-center', 'bg-gradient-to-tl', 'from-primary/30', 'via-primary-20', 'to-primary/10']

onMounted(() => {
  document.documentElement.classList.add(...bgTheme)
})

onUnmounted(() => {
  document.documentElement.classList.remove(...bgTheme)
})
</script>
