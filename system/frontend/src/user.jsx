// Who is signed in. FR-26 (sign out after the person's own idle time), FR-28 (sign in first).
import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import { get, post, live, getToken, setToken } from './api.js'

const UserContext = createContext({ user: null, ready: false })

export function UserProvider({ children }) {
  const [user, setUser] = useState(null)
  const [ready, setReady] = useState(false)

  const clear = useCallback((note) => {
    setToken('')
    live.disconnect()
    if (note) sessionStorage.setItem('fd-note', note)
    setUser(null)
  }, [])

  useEffect(() => {
    if (!getToken()) { setReady(true); return }
    get('/api/me').then((d) => { if (d.username) setUser(d) }).finally(() => setReady(true))
  }, [])

  useEffect(() => {
    const onUnauth = () => clear('Your sign-in ended. Please sign in again.')
    window.addEventListener('fd-unauth', onUnauth)
    return () => window.removeEventListener('fd-unauth', onUnauth)
  }, [clear])

  useEffect(() => { if (user) live.connect(); else live.disconnect() }, [user])

  // FR-26: signed out after this person's idle time. Only the person's own activity keeps the session alive.
  useEffect(() => {
    if (!user) return undefined
    let last = Date.now()
    let pinged = Date.now()
    const mark = () => { last = Date.now() }
    const events = ['mousemove', 'keydown', 'click', 'touchstart', 'scroll']
    events.forEach((e) => window.addEventListener(e, mark))
    const timer = setInterval(() => {
      if (Date.now() - last > user.session_min * 60000) {
        post('/api/signout')
        clear(`You were signed out after ${user.session_min} minute${user.session_min > 1 ? 's' : ''} without activity.`)
      } else if (last > pinged && Date.now() - pinged > 20000) {
        pinged = Date.now()
        post('/api/me/ping')
      }
    }, 5000)
    return () => { events.forEach((e) => window.removeEventListener(e, mark)); clearInterval(timer) }
  }, [user, clear])

  const signIn = async (username, password) => {
    const r = await post('/api/signin', { username, password })
    if (r.ok) { setToken(r.token); setUser(r.user) }
    return r
  }
  const signOut = async () => { await post('/api/signout'); clear() }

  return <UserContext.Provider value={{ user, ready, signIn, signOut, setUser }}>{children}</UserContext.Provider>
}

export const useUser = () => useContext(UserContext)
