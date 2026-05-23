<template>
  <div class="w-full h-[100px] flex justify-center items-end">
    <div v-for="i in 4" :key="i" class="loading-bar bg-primary-200 dark:bg-primary-800 w-5 h-2.5 rounded-sm my-0 mx-[5px]" />
  </div>
</template>

<style scoped>
.loading-bar {
  animation: loading-wave-animation 1s ease-in-out infinite;
}

.loading-bar:nth-child(2) {
  animation-delay: 0.1s;
}

.loading-bar:nth-child(3) {
  animation-delay: 0.2s;
}

.loading-bar:nth-child(4) {
  animation-delay: 0.3s;
}

@keyframes loading-wave-animation {
  0% {
    height: 10px;
  }

  50% {
    height: 50px;
  }

  100% {
    height: 10px;
  }
}
</style>
