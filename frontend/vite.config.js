import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { NodePackageImporter } from 'sass-embedded'
import { defineConfig, loadEnv } from 'vite'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig((config) => {
  const env = loadEnv(config.mode, process.cwd(), '')
  return {
    base: env.VITE_BASE_URL || '/',
    server: {
      proxy: {
        '/v1/api': {
          target: env.VITE_APP_API_URL,
          ws: true,
          changeOrigin: true,
          logLevel: 'debug',
        },
      },
    },
    plugins: [vue(), vueDevTools()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    css: {
      preprocessorOptions: {
        scss: {
          api: 'modern',
          importers: [new NodePackageImporter()],
        },
      },
    },
    build: {
      rollupOptions: {
        output: {
          manualChunks(id) {},
        },
      },
    },
  }
})
