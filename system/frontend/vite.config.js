import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Sends /api and the live connection to the Flask server on port 5000.
// If the server runs with HTTPS (see SETUP.md), start Vite with BACKEND=https://127.0.0.1:5000
const backend = process.env.BACKEND || 'http://127.0.0.1:5000'
const secure = false          // the demo certificate is made by the server itself

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': { target: backend, secure },
      '/socket.io': { target: backend, ws: true, secure },
    },
  },
})
