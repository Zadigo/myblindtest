/// <reference types="vitest" />

import { defineConfig, loadEnv } from 'vite'
import { resolve } from 'path'

import tailwind from '@tailwindcss/vite'
import unheadVite from '@unhead/addons/vite'
import eslint from 'vite-plugin-eslint'
import vue from '@vitejs/plugin-vue'
import unpluginViteComponents from 'unplugin-vue-components/vite'
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
      unheadVite(),
      tailwind(),
      unpluginViteComponents({
        deep: true,
        dts: 'src/types/components.d.ts',
        dirs: [
          'src/components'
        ],
        extensions: [
          'vue'
        ]
      }),
      autoImport({
        dts: 'src/types/auto-imports.d.ts',
        vueTemplate: true,
        imports: [
          'vue',
          'pinia',
          '@vueuse/core'
        ],
        dirs: [
          'src/plugins',
          'src/stores'
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
