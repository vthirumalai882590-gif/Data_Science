import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        // When the backend is not running, return a proper error response
        // so the browser fetch() try/catch can handle it, instead of crashing.
        configure: (proxy) => {
          proxy.on('error', (_err, _req, res: any) => {
            if (res && typeof res.writeHead === 'function') {
              res.writeHead(503, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({
                detail: 'Backend service unavailable — using embedded AI engine.',
                mode: 'embedded'
              }));
            }
          });
        },
      },
      '/static': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        configure: (proxy) => {
          proxy.on('error', (_err, _req, res: any) => {
            if (res && typeof res.writeHead === 'function') {
              res.writeHead(503, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ detail: 'Static assets unavailable.' }));
            }
          });
        },
      }
    }
  },
  preview: {
    port: 4173,
  },
})
