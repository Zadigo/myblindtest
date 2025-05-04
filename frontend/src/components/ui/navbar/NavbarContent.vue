<template>
  <div class="container flex flex-wrap items-center justify-between mx-auto text-slate-800">
    <div class="mr-4 block cursor-pointer py-1.5 text-1xl text-slate-800 font-bold uppercase">
      <slot name="brand">
        {{ brand }}
      </slot>
    </div>

    <div class="hidden lg:block">
      <slot />
    </div>

    <button id="action-menu" class="relative ml-auto h-6 max-h-[40px] w-6 max-w-[40px] select-none rounded-lg text-center align-middle text-xs font-medium uppercase text-inherit transition-all hover:bg-transparent focus:bg-transparent active:bg-transparent disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none lg:hidden" type="button">
      <span class="absolute transform -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { PrimitiveProps } from 'reka-ui'
import { HTMLAttributes } from 'vue'

interface Props extends PrimitiveProps {
  class?: HTMLAttributes['class']
  brand?: string
}

withDefaults(defineProps<Props>(), {
  brand: 'Vite'
})
</script>
