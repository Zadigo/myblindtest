<template>
  <volt-card>
    <template #title>
      <div class="flex items-center justify-between">
        <h3 class="font-bold">
          Jokers
        </h3>

        <volt-label label-for="activate-jokers">
          <volt-toggle-switch id="activate-jokers" :disabled="true" />
        </volt-label>
      </div>
    </template>

    <template #content>
      <div id="jokers" class="inner-shadow rounded-lg overflow-hidden">
        <div class="flex gap-2 p-5 overflow-x-scroll">
          <div v-for="idx in 9" :key="idx" class="border-2 border-primary-200 dark:border-primary-600 p-3 rounded-lg min-h-40 min-w-30 bg-primary-50 dark:bg-primary-700 cursor-pointer">
            1
          </div>
        </div>
      </div>
    </template>
  </volt-card>
</template>

<style scoped>
#jokers>div::-webkit-scrollbar {
  display: none;
}

.inner-shadow {
  box-shadow: inset 0 4px 24px var(--color-primary-100);
}

.dark .inner-shadow, .p-dark .inner-shadow {
  box-shadow: inset 0 4px 24px var(--color-primary-800);
}
</style>
