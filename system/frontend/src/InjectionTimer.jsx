// Countdown in the corner for a demo injection that has not started yet. Requirements: FR-11, FR-12 (demo)
// The server sends the start time with each snapshot. The count is worked out here against the server's clock.
import { useEffect, useRef, useState } from 'react'
import { post } from './api.js'

export default function InjectionTimer({ scheduled, serverTime }) {
  const offset = useRef(0)
  const prev = useRef([])
  const cancelled = useRef(new Set())
  const [started, setStarted] = useState([])
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => { if (serverTime) offset.current = serverTime - Date.now() / 1000 }, [serverTime])
  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 200)
    return () => clearInterval(timer)
  }, [])
  useEffect(() => {
    const list = scheduled ?? []
    const ids = new Set(list.map((i) => i.id))
    const gone = prev.current.filter((i) => !ids.has(i.id) && !cancelled.current.has(i.id))
    prev.current = list
    if (gone.length) setStarted((s) => [...s, ...gone.map((i) => ({ id: i.id, label: i.label, until: Date.now() + 5000 }))])
  }, [scheduled])

  const nowS = now / 1000 + offset.current
  const shown = started.filter((s) => s.until > now)
  if (!(scheduled?.length) && shown.length === 0) return null
  return (
    <div className="timer-corner">
      {(scheduled ?? []).map((i) => {
        const left = Math.max(0, i.at - nowS)
        return (
          <div className="card timer-item" key={i.id}>
            <div className="timer-count" aria-hidden="true">{Math.ceil(left)}</div>
            <div className="timer-text">
              <strong>{left > 0 ? `Starts in ${Math.ceil(left)} s` : 'Starting now'}</strong>
              <span>{i.label}</span>
            </div>
            <button className="demo-btn demo-btn-off" onClick={() => { cancelled.current.add(i.id); post('/api/demo', { action: 'cancel', schedule_id: i.id }) }}>Cancel</button>
          </div>
        )
      })}
      {shown.map((s) => (
        <div className="card timer-item timer-started" key={`s${s.id}`}><div className="timer-text"><strong>Started</strong><span>{s.label}</span></div></div>
      ))}
    </div>
  )
}
