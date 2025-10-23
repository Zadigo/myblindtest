<template>
  <!-- animate-bounce animate-ease-in-out animate-duration-1000 -->
  <div ref="dock" id="dock" class="col-span-12 bg-primary-100/30 border border-primary-100/80 h-auto min-w-100 w-150 absolute bottom-10 left-[calc(50%-calc(600px/2))] p-2 rounded-xl flex justify-center gap-2 z-40">
    <div v-for="action in actions" :key="action.icon" class="p-1 bg-primary-50 rounded-lg w-13 h-13 flex justify-center items-center gap-2 cursor-pointer hover:bg-primary-100 transition hover:-translate-y-1" @click="action.action">
      <vue-icon :icon="action.icon" class="text-xl" />
    </div>
  </div>
</template>

<script setup lang="ts">
const actions = [
  { icon: 'lucide:play', action: () => console.log('Play') },
  { icon: 'lucide:pause', action: () => console.log('Pause') },
  { icon: 'lucide:circle-stop', action: () => console.log('Stop') },
  { icon: 'lucide:zap', action: () => console.log('Stop') }
]
</script>
