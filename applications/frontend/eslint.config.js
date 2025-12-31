import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import eslintPluginReact from 'eslint-plugin-react';
import eslintPluginReactHooks from 'eslint-plugin-react-hooks';
import eslintConfigPrettier from 'eslint-config-prettier';
import eslintPluginImport from 'eslint-plugin-import';
import eslintPluginUnusedImports from 'eslint-plugin-unused-imports';
import globals from 'globals';

export default tseslint.config(
  {
    name: 'typescript-react-app/ignore-patterns',
    ignores: [
      '**/node_modules',
      '**/dist',
      '**/build',
    ],
  },
  {
    name: 'typescript-react-app/base-config',
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      import: eslintPluginImport,
      'unused-imports': eslintPluginUnusedImports,
      react: eslintPluginReact,
      'react-hooks': eslintPluginReactHooks,
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
  },
  {
    name: 'typescript-react-app/global-rules',
    extends: [
      eslint.configs.recommended,
    ],
    rules: {
      'import/order': 'error',
      'unused-imports/no-unused-imports': 'error',
      'unused-imports/no-unused-vars': [
        'error',
        {
          vars: 'all',
          varsIgnorePattern: '^_',
          args: 'after-used',
          argsIgnorePattern: '^_',
        },
      ],
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },
  {
    name: 'typescript-react-app/typescript-rules',
    files: ['**/*.ts', '**/*.tsx'],
    extends: [
      tseslint.configs.strict,
      eslintPluginReact.configs.flat.recommended,
      eslintPluginReact.configs.flat['jsx-runtime'],
    ],
    rules: {
      '@typescript-eslint/no-unused-vars': 'off',
      '@typescript-eslint/no-explicit-any': 'error',
      'react/prop-types': 'off',
      ...eslintPluginReactHooks.configs.recommended.rules,
    },
  },
  {
    name: 'typescript-react-app/prettier-config',
    ...eslintConfigPrettier,
  }
);