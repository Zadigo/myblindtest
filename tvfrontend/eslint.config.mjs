import globals from 'globals'
import eslint from '@eslint/js'
import eslintPluginVue from 'eslint-plugin-vue'
import typescriptEslint from 'typescript-eslint'
import stylistic from '@stylistic/eslint-plugin'

export default typescriptEslint.config(
  { 
    ignores: [
      '*.d.ts', 
      '**/coverage', 
      '**/dist', 
      '**/src/volt/**',
      '**/src/components/ui/**'
    ]
  },
  {
    plugins: {
      '@stylistic': stylistic,
    },
    extends: [
      stylistic.configs.recommended,
      eslint.configs.recommended,
      ...typescriptEslint.configs.recommended,
      ...eslintPluginVue.configs['flat/recommended'],
    ],
    files: ['**/*.{ts,vue}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: globals.browser,
      parserOptions: {
        parser: typescriptEslint.parser,
        projectService: true,
        extraFileExtensions: ['.vue']
      }
    },
    rules: {
      'vue/max-attributes-per-line': ['error', {
        'singleline': {
          "max": 20
        },
        'multiline': {
          "max": 1
        }
      }],
      "vue/multi-word-component-names": ['warn'],
      "vue/no-v-html": ['warn'],

      "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
      '@typescript-eslint/unified-signatures': 'error',
      '@typescript-eslint/related-getter-setter-pairs': 'warn',
      '@typescript-eslint/no-unnecessary-type-arguments': 'warn',
      '@typescript-eslint/no-unnecessary-template-expression': 'warn',
      '@typescript-eslint/no-unnecessary-condition': 'warn',
      '@typescript-eslint/no-unnecessary-boolean-literal-compare': 'warn',
      '@typescript-eslint/no-non-null-assertion': 'warn',
      '@typescript-eslint/no-non-null-asserted-nullish-coalescing': 'warn',
      '@typescript-eslint/no-misused-spread': 'warn',
      '@typescript-eslint/no-extraneous-class': 'warn',

      '@stylistic/no-trailing-spaces': ['warn'],
      '@stylistic/comma-dangle': ['warn', 'never'],
      '@stylistic/brace-style': ['error', '1tbs'],
      '@stylistic/no-confusing-arrow': ['warn'],
      '@stylistic/switch-colon-spacing': [
        'error', { 'after': true, 'before': false }
      ]
    }
  }
)
