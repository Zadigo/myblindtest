import tailwind from '@tailwindcss/vite'
import unheadVite from '@unhead/addons/vite'
import vue from '@vitejs/plugin-vue'
import autoImport from 'unplugin-auto-import/vite'
import autoImportComponents from 'unplugin-vue-components/vite'
import eslint from 'vite-plugin-eslint2'

import { resolve } from 'path'
import { PrimeVueResolver } from 'unplugin-vue-components/resolvers'
import { defineConfig, loadEnv } from 'vite'

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
      unheadVite(),
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
          'vue',
          'pinia',
          '@vueuse/core'
        ],
        dirs: [
          'src/plugins',
          'src/stores'
        ]
      })
    ]
  }
})
