import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Sends /api and the live connection to the Flask server on port 5000.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:5000',
      '/socket.io': { target: 'http://127.0.0.1:5000', ws: true },
    },
  },
})
