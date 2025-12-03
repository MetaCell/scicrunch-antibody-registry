import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const proxyTarget = env && env.DOMAIN ? env.DOMAIN : 'http://localhost:8000';
  return {
    plugins: [react()],
    
    resolve: {
      alias: {
        // Match the babel module-resolver root configuration
        '@': path.resolve(__dirname, './src'),
      },
      extensions: ['.js', '.jsx', '.ts', '.tsx', '.json'],
    },
    
    build: {
      outDir: 'dist',
      sourcemap: true,
      rollupOptions: {
        output: {
          manualChunks: undefined,
        },
      },
    },
    
    server: {
      port: 9100,
      host: true,
      proxy: {
        '/api': {
          target: proxyTarget,
          changeOrigin: true,
          secure: false
        },
        '/proxy/accounts-api': {
          target:env.ACCOUNTS_API_DOMAIN || env.DOMAIN?.replace('portal', 'api.accounts') || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/proxy\/accounts-api/, ''),
          configure: (proxy) => {
            proxy.on('proxyReq', (proxyReq, req) => {
              proxyReq.setHeader('Cookie', req.headers.cookie || '');
            });
          },
        },
        '/media': {
          target: process.env.VITE_DOMAIN || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          configure: (proxy) => {
            proxy.on('proxyReq', (proxyReq, req) => {
              proxyReq.setHeader('Cookie', req.headers.cookie || '');
            });
          },
        },
      },
    },
  };
});
