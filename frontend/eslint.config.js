import js from '@eslint/js'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'
import pluginVue from 'eslint-plugin-vue'

export default [
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,jsx,vue}'],
    root: true,
    env: {
      node: true,
    },
    extends: [js.configs.recommended, ...pluginVue.configs['flat/essential'], skipFormatting],
    parserOptions: {
      parser: '@babel/eslint-parser',
    },
    rules: {
      indent: 'off',
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'space-before-function-paren': [
        'error',
        {
          anonymous: 'always',
          named: 'never',
          asyncArrow: 'always',
        },
      ],
      'vue/no-deprecated-v-bind-sync': 'off',
      'vue/no-v-for-template-key-on-child': 'off',
      'vue/no-deprecated-destroyed-lifecycle': 'off',
      'vue/multi-word-component-names': 'off',
      'vue/no-unused-components': 'warn',
      'vue/no-unused-vars': 'warn',
    },
  },

  {
    name: 'app/files-to-ignore',
    ignores: ['**/dist/**', '**/dist-ssr/**', '**/coverage/**'],
  },
]
