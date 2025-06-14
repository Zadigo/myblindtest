/// <reference types="vitest" />

import { unheadVueComposablesImports } from '@unhead/vue'
import { defineConfig, loadEnv } from 'vite'
import { resolve } from 'path'
import { PrimeVueResolver } from 'unplugin-vue-components/resolvers'

import tailwind from '@tailwindcss/vite'
import eslint from 'vite-plugin-eslint'
import vue from '@vitejs/plugin-vue'
import autoImportComponents from 'unplugin-vue-components/vite'
import autoImport from 'unplugin-auto-import/vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const root = process.cwd()
  const env = loadEnv(mode, root)
  process.env = { ...process.env, ...env }

  return {
    root,
    resolve: {
      alias: [
        {
          find: '@',
          replacement: resolve(__dirname, 'src')
        }
      ]
    },
    plugins: [
      vue(),
      eslint(),
      tailwind(),
      autoImportComponents({
        deep: true,
        dts: 'src/types/components.d.ts',
        dirs: [
          'src/components',
          'src/layouts'
        ],
        exclude: [
          'src/components/ui/'
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
        imports: [
          unheadVueComposablesImports,
          'vue',
          'pinia',
          '@vueuse/core'
        ],
        dirs: [
          'src/composables',
          'src/plugins',
          'src/stores',
          'src/data'
        ]
      })
    ],
    test: {
      globals: true,
      environment: 'happy-dom',
      setupFiles: 'tests/setupVuetify.ts',
      css: true,
      pool: 'vmThreads',
      // deps.optimizer.web.include
      // server.deps.inline
      server: {
        deps: {
          inline: ['vuetify']
        }
      }
    }
  }
})
