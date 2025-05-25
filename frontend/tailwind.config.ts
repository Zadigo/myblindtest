import animate from 'tw-animate-css'

import type { Config } from 'tailwindcss'

export default {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
    './error.vue',
    './nuxt.config.{js,ts}'
  ],
  theme: {
    extend: {
      fontFamily: {},
      colors: {},
      screens: {}
    }
  },
  plugins: [
    animate
  ], 
  darkMode: 'class'
} as Config
