// Talks to the Flask server. The live connection carries the readings (stream 1) and the statuses.
import { io } from 'socket.io-client'

export async function get(path) {
  const r = await fetch(path)
  return r.json()
}

export async function post(path, body) {
  const r = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
  return r.json()
}

export const live = io({ autoConnect: false })
