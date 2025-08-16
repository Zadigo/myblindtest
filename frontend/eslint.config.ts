import js from '@eslint/js'
import stylistic from '@stylistic/eslint-plugin'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'
import tseslint from 'typescript-eslint'
import autoImportGlobals from './.eslintrc-auto-import.json'

import { defineConfig } from 'eslint/config'

// https://stackoverflow.com/questions/58510287/parseroptions-project-has-been-set-for-typescript-eslint-parser

export default defineConfig([
  stylistic.configs.recommended,
  tseslint.configs.recommended,
  // pluginVue.configs['flat/strongly-recommended'],

  {
    rules: {
      '@stylistic/comma-dangle': ['warn', 'never'],
      '@stylistic/brace-style': ['error', '1tbs'],
      '@stylistic/no-confusing-arrow': ['warn'],
      '@stylistic/switch-colon-spacing': ['error', { after: true, before: false }]
    }
  }
])
