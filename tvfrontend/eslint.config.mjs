// @ts-check
// import eslintjs from '@eslint/js'
// import stylistic from '@stylistic/eslint-plugin'
// import vueEslint from 'eslint-plugin-vue'
import globals from 'globals'
import tseslint from 'typescript-eslint'
import autoImportGlobals from './.eslintrc-auto-import.json' with { type: 'json' }

// import { defineConfig } from 'eslint/config'

export default tseslint.config(
  {
    ignores: [
      '**/*.d.ts',
      '**/coverage',
      '**/dist',
      '**/*.js',
      'node_modules'
    ],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...autoImportGlobals.globals
      }
    }
  },
  tseslint.configs.recommended,
  // tseslint.configs.strict,
  tseslint.configs.stylistic,
  // eslintjs.configs.recommended,
  // {
  //   files: ['src/**/*.vue'],
  //   extends: [
  //     tseslint.configs.recommended,
  //     vueEslint.configs['flat/strongly-recommended']
  //   ],
  //   languageOptions: {
  //     parser: vueEslint.parser
  //   },
  //   rules: {
  //     'vue/multi-word-component-names': 'off',
  //     'vue/max-attributes-per-line': ['error', {
  //       singleline: {
  //         max: 20
  //       },
  //       multiline: {
  //         max: 1
  //       }
  //     }]
  //   }
  // },
  // {
  //   files: ['src/**/*.{ts}'],
  //   languageOptions: {
  //     parser: tseslint.parser,
  //   }
  // },
  // {
  //   extends: [
  //     stylistic.configs.recommended
  //   ],
  //   languageOptions: {
  //     parserOptions: {
  //       tsconfigRootDir: import.meta.dirname,
  //       projectService: true
  //     }
  //   },
  //   rules: {
  //     '@stylistic/comma-dangle': ['warn', 'never'],
  //     '@stylistic/brace-style': ['error', '1tbs'],
  //     '@stylistic/no-confusing-arrow': ['warn'],
  //     '@stylistic/switch-colon-spacing': ['error', { after: true, before: false }],
  //   }
  // }
)
