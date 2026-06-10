<template>
  <section id="site">
    <!-- Toast -->
    <volt-toast />
    <!-- Main -->
    <router-view v-slot="{ Component }">
      <transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 -translate-x-10" enter-to-class="opacity-100 translate-x-0" leave-active-class="duration-300 ease-in" leave-from-class="opacity-100 translate-x-0" leave-to-class="opacity-0 translate-x-10" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </section>
</template>

<script setup lang="ts">
</script>
