<template>
  <section class="h-screen">
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
              Home
            </router-link>
          </navbar-link>

          <navbar-link>
            <router-link :to="{ name: 'create' }">
              Create
            </router-link>
          </navbar-link>

          <navbar-link>
            <router-link :to="{ name: 'create' }">
              About
            </router-link>
          </navbar-link>
        </navbar-links>
      </navbar-content>
    </navbar>

    <Toaster position="top-right" />

    <!-- Main -->
    <router-view v-slot="{ Component }">
      <Transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 -translate-x-10 blur-sm" enter-to-class="opacity-100 translate-x-0 blur-none" leave-active-class="duration-300 ease-in" leave-from-class="opacity-100 translate-x-0 blur-none" leave-to-class="opacity-0 translate-x-10 blur-sm" mode="out-in">
        <component :is="Component" />
      </Transition>
    </router-view>
  </section>
</template>

<script setup lang="ts">
const bgTheme = ref<string[]>(['dark:bg-primary-950', 'bg-no-repeat', 'bg-center', 'bg-gradient-to-tl', 'from-primary/30', 'via-primary-20', 'to-primary/10'])

onMounted(() => {
  document.documentElement.classList.add(...bgTheme.value)
})
onUnmounted(() => {
  document.documentElement.classList.remove(...bgTheme.value)
})
</script>
