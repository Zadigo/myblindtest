<template>
  <nav :class="cn(navbarVariants({ variant, size }), props.class)">
    <slot />
  </nav>
</template>

<script setup lang="ts">
import { cn } from '@/lib/utils'
import { type NavbarVariants, navbarVariants } from './index'

import { type PrimitiveProps } from 'reka-ui'
import { type HTMLAttributes } from 'vue'

interface Props extends PrimitiveProps {
  variant?: NavbarVariants['variant'],
  size?: NavbarVariants['size'],
  class?: HTMLAttributes['class']
}

const props = withDefaults(defineProps<Props>(), {})
</script>
