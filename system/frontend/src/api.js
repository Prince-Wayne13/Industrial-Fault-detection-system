// Talks to the Flask server. Every call carries the sign-in token (FR-28). The live connection carries the readings (stream 1) and the statuses.
import { io } from 'socket.io-client'

const KEY = 'fd-token'            // sessionStorage: each browser tab is its own sign-in, so two people can be shown on one laptop
export const getToken = () => sessionStorage.getItem(KEY) || ''
export const setToken = (t) => (t ? sessionStorage.setItem(KEY, t) : sessionStorage.removeItem(KEY))

async function call(method, path, body) {
  const r = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` },
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  if (r.status === 401 && getToken()) window.dispatchEvent(new Event('fd-unauth'))
  return r.json().catch(() => ({ ok: false, message: 'The server sent a reply that could not be read.' }))
}

export const get = (path) => call('GET', path)
export const post = (path, body = {}) => call('POST', path, body)
export const del = (path) => call('DELETE', path)

// A file download that carries the token in the header, never in the address.
export async function download(path, filename) {
  const r = await fetch(path, { headers: { Authorization: `Bearer ${getToken()}` } })
  if (!r.ok) return r.json().catch(() => ({ ok: false, message: 'Could not make the file.' }))
  const url = URL.createObjectURL(await r.blob())
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
  return { ok: true }
}

export const live = io({ autoConnect: false, auth: (cb) => cb({ token: getToken() }) })
