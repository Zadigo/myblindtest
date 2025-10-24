<template>
  <section v-if="meta.title === 'Home'" id="home">
    <router-view />
  </section>

  <section v-else id="interface" class="relative">
    <div class="px-10 flex justify-center items-center">
      <router-view />
    </div>
  </section>
</template> 

<script setup lang="ts">
const meta = useRoute().meta as { title: string }
</script>
