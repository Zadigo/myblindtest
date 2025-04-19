/// <reference types="vitest" />

import { defineConfig, loadEnv } from 'vite'
import { resolve } from 'path'

import tailwind from '@tailwindcss/vite'
import UnheadVite from '@unhead/addons/vite'
import eslint from 'vite-plugin-eslint'
import vue from '@vitejs/plugin-vue'

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
      UnheadVite(),
      tailwind()
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
