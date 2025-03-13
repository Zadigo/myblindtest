import tailwind from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import eslint from 'vite-plugin-eslint'
import unhead from '@unhead/addons/vite'

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
      unhead()
    ],
    resolve: {
      alias: [
        {
          find: "@",
          replacement: resolve(__dirname, "src"),
        },
        {
          find: "src",
          replacement: resolve(__dirname, 'src')
        }
      ],
    },
  }
})
