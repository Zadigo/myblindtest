import { defineConfig } from 'vitest/config'
import { defineVitestProject } from '@nuxt/test-utils/config'

export default defineConfig({
  test: {
    setupFiles: ['./tests/setup.ts'],
    exclude: [
      'node_modules',
      '.nuxt', 
      'dist', 
      'tests/__fixtures__', 
      'tests/e2e'
    ],
    coverage: {
      enabled: true,
      provider: 'v8',
      reporter: [ 'text', 'json', 'html' ]
    },
    env: {
      NODE_ENV: 'test'
    },
    projects: [
      await defineVitestProject({
        test: {
          name: 'nuxt',
          include: [ 'tests/nuxt/**/*.{test,spec}.ts' ],
          environment: 'nuxt',
          testTimeout: 20000,
          tags: [
            {
              name: 'nuxt',
            },
            {
              name: 'composable',
              description: 'Tests for composables'
            },
            {
              name: 'frontend',
              description: 'Tests for frontend components'
            },
            {
              name: 'server',
              description: 'Tests for server-side components'
            }
          ]
        }
      }),
      await defineVitestProject({
        test: {
          name: 'integration',
          include: ['tests/integration/**/*.{test,spec}.ts'],
          environment: 'node',
          testTimeout: 20000,
          tags: [
            {
              name: 'integration',
            }
          ]
        }
      })
    ]
  },
  resolve: {}
})
