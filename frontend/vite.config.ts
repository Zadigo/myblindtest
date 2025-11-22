import { fileURLToPath, URL } from 'node:url'
import biome from 'vite-plugin-biome'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

import tailwind from '@tailwindcss/vite'
import { PrimeVueResolver } from 'unplugin-vue-components/resolvers'
import { unheadVueComposablesImports } from '@unhead/vue'
import componentsAutoImport from 'unplugin-vue-components/vite'
import globalAutoImport from 'unplugin-auto-import/vite'

// https://vite.dev/config/
export default defineConfig({
  server: {
    allowedHosts: ['.ngrok-free.app']
  },
  plugins: [
    vue(),
    tailwind(),
    vueDevTools(),
    biome(),
    componentsAutoImport({
      deep: true,
      dts: 'src/types/components.d.ts',
      dirs: [
        'src/components',
        'src/layouts'
      ],
      resolvers: [
        PrimeVueResolver({
          prefix: 'Volt'
        })
      ],
      extensions: [
        'vue'
      ]
    }),
    globalAutoImport({
      dts: 'src/types/auto-imports.d.ts',
      vueTemplate: true,
      eslintrc: {
        enabled: true,
        filepath: '.eslintrc-auto-import.json',
        globalsPropValue: true
      },
      imports: [
        unheadVueComposablesImports,
        'vue',
        'pinia',
        '@vueuse/core',
        {
          'vue-router': [
            'useRoute',
            'useRouter',
            'onBeforeRouteLeave',
            'onBeforeRouteUpdate'
          ]
        },
        {
          'vue-axios-manager': [
            'useRequest',
            'useAsyncRequest',
          ]
        }
      ],
      dirs: [
        'src/composables',
        'src/plugins',
        'src/stores',
        'src/data',
        'src/utils'
      ]
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
