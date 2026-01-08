import tailwind from '@tailwindcss/vite'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  modules: [
    '@nuxt/a11y',
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/hints',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@vueuse/nuxt',
    '@vueuse/motion',
    '@pinia/nuxt',
    '@nuxtjs/i18n',
    'nuxt-vuefire',
    'nuxt-charts'
  ],

  ssr: false,

  routeRules: {
    '/': { swr: true },
    '/blindtest/**': { },
    '/create-songs': { swr: true },
    '/statistics': { swr: true },
    '/logs ': { swr: true },
    '/about': { prerender: true }
  },

  app: {
    pageTransition: { name: 'page', mode: 'out-in' }
  },

  vite: {
    plugins: [tailwind()]
  },

  vuefire: {
    config: {
      apiKey: process.env.NUXT_PUBLIC_FIREBASE_API_KEY,
      authDomain: process.env.NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
      projectId: process.env.NUXT_PUBLIC_FIREBASE_PROJECT_ID,
      storageBucket: process.env.NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
      messagingSenderId: process.env.NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
      appId: process.env.NUXT_PUBLIC_FIREBASE_APP_ID,
      measurementId: process.env.NUXT_PUBLIC_FIREBASE_MEASUREMENT_ID
    }
  },

  fonts: {
    families: [
      {
        name: 'Inria Sans'
      },
      {
        name: 'Raleway'
      }
    ]
  },

  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL
    }
  },

  css: [
    '~/assets/css/main.css'
  ],

  i18n: {
    baseUrl: process.env.NUXT_PUBLIC_SITE_URL,
    langDir: './locales',
    defaultLocale: 'fr',
    vueI18n: './i18n.config.ts',
    customRoutes: 'config',
    pages: {

    },
    locales: [
      {
        code: 'fr',
        language: 'fr-FR',
        file: 'fr-FR.ts',
        dir: 'ltr',
        name: 'French'
      },
      {
        code: 'en',
        language: 'en-US',
        files: ['en.ts', 'en-US.ts'],
        dir: 'ltr',
        name: 'English'
      }
    ]
  },

  // eslint: {
  //   config: {
  //     stylistic: {
  //       commaDangle: 'never',
  //       braceStyle: '1tbs'
  //     }
  //   }
  // }
})
