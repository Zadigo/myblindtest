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
    <router-view />
  </section>
</template>

<script setup lang="ts">
const bgTheme = ref<string[]>(['bg-no-repeat', 'bg-center', 'bg-gradient-to-tl', 'from-primary/30', 'via-primary-20', 'to-primary/10'])

onMounted(() => {
  document.documentElement.classList.add(...bgTheme.value)
})
onUnmounted(() => {
  document.documentElement.classList.remove(...bgTheme.value)
})
</script>
