import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/projects':  'http://localhost:8000',
      '/process':   'http://localhost:8000',
      '/recommend': 'http://localhost:8000',
      '/analytics': 'http://localhost:8000',
    },
  },
})
