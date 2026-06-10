<template>
  <volt-card>
    <template #title>
      <div class="flex items-center justify-between">
        <h3 class="font-bold">
          Jokers
        </h3>

        <form>
          <volt-label label-for="activate-jokers">
            <volt-toggle-switch id="activate-jokers" :disabled="true" />
          </volt-label>
        </form>
      </div>
    </template>

    <template #content>
      <div id="jokers" class="inner-shadow rounded-lg overflow-hidden">
        <div class="flex gap-2 p-5 overflow-x-scroll">
          <div v-for="idx in 9" :key="idx" class="p-5 border-2 border-primary-200 dark:border-primary-600 rounded-lg min-h-50 min-w-40 overflow-hidden hover:border-2 hover:-translate-y-1.5 transition-all ease-in-out bg-primary-50 dark:bg-primary-700 cursor-pointer">
            <div class="flex flex-wrap items-center w-full h-full">
              <h4 class="font-bold text-2xl">Pour l'humanité</h4>
            </div>
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
