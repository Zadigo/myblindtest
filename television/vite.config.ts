import { fileURLToPath, URL } from 'node:url'
import tailwind from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import autoImport from 'unplugin-auto-import/vite'
import { PrimeVueResolver } from 'unplugin-vue-components/resolvers'
import { unheadVueComposablesImports } from '@unhead/vue'
import autoImportComponents from 'unplugin-vue-components/vite'
import { defineConfig } from 'vite'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    tailwind(),
    autoImportComponents({
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
    autoImport({
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
          'vue-axios-manager': [
            'useRequest'
          ]
        },
        {
          'vue-router': [
            'useRouter',
            'useRoute'
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
