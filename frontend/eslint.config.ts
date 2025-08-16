import eslintjs from '@eslint/js'
import stylistic from '@stylistic/eslint-plugin'
import vueEslint from 'eslint-plugin-vue'
import globals from 'globals'
import tseslint from 'typescript-eslint'
import autoImportGlobals from './.eslintrc-auto-import.json'

import { defineConfig } from 'eslint/config'

export default tseslint.config(
  {
    ignores: [
      '*.d.ts',
      '**/coverage',
      '**/dist',
      '*.config.ts'
    ]
  },
  eslintjs.configs.recommended,
  tseslint.configs.recommended,
  tseslint.configs.strict,
  tseslint.configs.stylistic
)

// export default tseslint.config(
//   {
//     ignores: [
//       '*.d.ts',
//       '**/coverage',
//       '**/dist'
//     ]
//   },
//   stylistic.configs.recommended,
//   js.configs.recommended,
//   tseslint.configs.recommended,
//   vueEslint.configs['flat/strongly-recommended'],
//   {
//     files: ['**/*.{ts,vue}'],
//     plugins: {
//       '@stylistic': stylistic
//     },
//     extends: [
//     ],
//     languageOptions: {
//       sourceType: 'module',
//       globals: { ...globals.browser, ...autoImportGlobals.globals },
//       parserOptions: {
//         ecmaVersion: 'latest',
//         extraFileExtensions: ['.vue']
//       }
//     },
//     rules: {
//       '@stylistic/comma-dangle': ['warn', 'never'],
//       '@stylistic/brace-style': ['error', '1tbs'],
//       '@stylistic/no-confusing-arrow': ['warn'],
//       '@stylistic/switch-colon-spacing': ['error', { after: true, before: false }],

//       '@typescript-eslint/no-unsafe-argument': 'warn',
//       '@typescript-eslint/unified-signatures': 'error',
//       '@typescript-eslint/related-getter-setter-pairs': 'warn',
//       '@typescript-eslint/no-unnecessary-type-arguments': 'warn',
//       '@typescript-eslint/no-unnecessary-template-expression': 'warn',
//       '@typescript-eslint/no-unnecessary-condition': 'warn',
//       '@typescript-eslint/no-unnecessary-boolean-literal-compare': 'warn',
//       '@typescript-eslint/no-non-null-assertion': 'warn',
//       '@typescript-eslint/no-non-null-asserted-nullish-coalescing': 'warn',
//       '@typescript-eslint/no-misused-spread': 'warn',
//       '@typescript-eslint/no-extraneous-class': 'warn'
//     }
//   },
//   {
//     files: [
//       '**/*.vue',
//       'eslint.config.ts'
//     ],
//     languageOptions: {
//       globals: {
//         ...globals.browser,
//         ...autoImportGlobals.globals
//       },
//       parser: vueEslint.parser,
//     },
//     rules: {
//       '@typescript-eslint/no-unsafe-argument': 'off'
//     }
//   },
//   {
//     files: ['eslint.config.ts'],
//     rules: {
//       '@typescript-eslint/no-unsafe-argument': 'off',
//       '@typescript-eslint/related-getter-setter-pairs': 'off',
//       '@typescript-eslint/no-unnecessary-type-arguments': 'off',
//       '@typescript-eslint/no-unnecessary-template-expression': 'off',
//       '@typescript-eslint/no-unnecessary-condition': 'off',
//       '@typescript-eslint/no-unnecessary-boolean-literal-compare': 'off',
//       '@typescript-eslint/no-misused-spread': 'off'
//     }
//   }
// )

// export default [
//   // add more generic rulesets here, such as:
//   // js.configs.recommended,
//   ...pluginVue.configs['flat/recommended'],
//   // ...pluginVue.configs['flat/vue2-recommended'], // Use this if you are using Vue.js 2.x.
//   {
//     rules: {
//       // override/add rules settings here, such as:
//       // 'vue/no-unused-vars': 'error'
//     },
//     languageOptions: {
//       sourceType: 'module',
//       globals: {
//         ...globals.browser
//       }
//     }
//   }
// ]

// https://stackoverflow.com/questions/58510287/parseroptions-project-has-been-set-for-typescript-eslint-parser

// export default defineConfig([
//   {
//     files: ['**/*.{js,ts,vue}'],
//     plugins: { js },
//     extends: ['js/recommended'],
//     languageOptions: {
//       globals: {
//         ...globals.browser,
//         ...autoImportGlobals.globals
//       }
//     }
//   },
//   stylistic.configs.recommended,
//   tseslint.configs.recommended,
//   // pluginVue.configs['flat/strongly-recommended'], // FIXME: Creates circular error
//   {
//     rules: {
//       '@stylistic/comma-dangle': ['warn', 'never'],
//       '@stylistic/brace-style': ['error', '1tbs'],
//       '@stylistic/no-confusing-arrow': ['warn'],
//       '@stylistic/switch-colon-spacing': ['error', { after: true, before: false }]
//     },
//     languageOptions: {
//       sourceType: 'module',
//       globals: {
//         ...globals.browser
//       }
//     }
//   },
//   // {
//   //   files: ['**/*.vue'],
//   //   plugins: { pluginVue },
//   //   extends: ['pluginVue/flat/strongly-recommended'],
//   //   rules: {
//   //     'vue/multi-word-component-names': 'off',
//   //     'vue/max-attributes-per-line': ['error', {
//   //       singleline: {
//   //         max: 20
//   //       },
//   //       multiline: {
//   //         max: 1
//   //       }
//   //     }]
//   //   }
//   // }
// ])

// [
//   {
//     files: ['**/*.{js,ts}'],
//     plugins: { js },
//     extends: ['js/recommended'],
//     languageOptions: {
//       globals: {
//         ...globals.browser,
//         ...autoImportGlobals.globals
//       },
//       parserOptions: {
//         projectService: true,
//         tsconfigRootDir: import.meta.dirname
//       }
//     }
//   },
//   pluginVue.configs['flat/strongly-recommended'],
//   // {
//   //   // ignorePatterns: [
//   //   //   '**/main.ts'
//   //   // ],
//   //   rules: {

//   //     '@typescript-eslint/no-unsafe-argument': 'warn',
//   //     '@typescript-eslint/unified-signatures': 'error',
//   //     '@typescript-eslint/related-getter-setter-pairs': 'warn',
//   //     '@typescript-eslint/no-unnecessary-type-arguments': 'warn',
//   //     '@typescript-eslint/no-unnecessary-template-expression': 'warn',
//   //     '@typescript-eslint/no-unnecessary-condition': 'warn',
//   //     '@typescript-eslint/no-unnecessary-boolean-literal-compare': 'warn',
//   //     '@typescript-eslint/no-non-null-assertion': 'warn',
//   //     '@typescript-eslint/no-non-null-asserted-nullish-coalescing': 'warn',
//   //     '@typescript-eslint/no-misused-spread': 'warn',
//   //     '@typescript-eslint/no-extraneous-class': 'warn',
//   //   }
//   // },

//   {
//     files: ['**/*.vue'],
//     languageOptions: {
//       globals: {
//         ...globals.browser,
//         ...autoImportGlobals.globals
//       },
//       parserOptions: {
//         projectService: true,
//         tsconfigRootDir: import.meta.dirname,
//         extraFileExtensions: ['.vue'],
//         parser: tseslint.parser
//       }
//     },
//     rules: {
//       '@typescript-eslint/no-unsafe-argument': 'off',
//       'vue/multi-word-component-names': 'off',
//       'vue/max-attributes-per-line': ['error', {
//         singleline: {
//           max: 20
//         },
//         multiline: {
//           max: 1
//         }
//       }]
//     }
//   },
// ]
