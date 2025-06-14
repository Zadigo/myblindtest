import tailwind from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import eslint from 'vite-plugin-eslint'
import unheadVite from '@unhead/addons/vite'
import autoImportComponents from 'unplugin-vue-components/vite'
import autoImport from 'unplugin-auto-import/vite'

import { PrimeVueResolver } from 'unplugin-vue-components/resolvers'
import { resolve } from 'path'
import { defineConfig, loadEnv } from 'vite'
// import eslint from 'vite-plugin-eslint2'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const root = process.cwd()
  const env = loadEnv(mode, root)
  process.env = { ...process.env, ...env }

  return {
    root,
    plugins: [
      vue(),
      eslint(),
      tailwind(),
      unheadVite(),
      autoImportComponents({
        deep: true,
        dts: 'src/types/components.d.ts',
        dirs: [
          'src/components'
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
    resolve: {
      alias: [
        {
          find: '@',
          replacement: resolve(__dirname, 'src')
        }
      ]
    }
  }
})
