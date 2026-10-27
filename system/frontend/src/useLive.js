// Keeps the Overview in step with the server. Readings arrive straight from the live connection (stream 1),
// statuses the moment a window closes (stream 2), and a full snapshot each second carries the marks.
import { useEffect, useState } from 'react'
import { get, live } from './api.js'
import { worst } from './status.js'

function patchReading(data, r) {
  return {
    ...data,
    machines: data.machines.map((m) => {
      const p = m.parameters[r.parameter]
      if (m.id !== r.machine_id || !p) return m
      const value = typeof r.value === 'number' ? r.value : null
      let window = p.window
      if (r.valid && value !== null) {
        const length = window?.length ?? 10
        let start = window?.start ?? null
        let readings = window?.readings ?? []
        if (start === null || r.time - start >= length) { start = r.time; readings = [] }   // the reading that ends a window starts the next one
        window = { start, length, readings: [...readings, [r.time, value, r.level]] }
      }
      return { ...m, parameters: { ...m.parameters, [r.parameter]: { ...p, value, invalid: !r.valid, sensor_fault: false, window } } }
    }),
  }
}

function patchStatus(data, w) {
  return {
    ...data,
    machines: data.machines.map((m) => {
      const p = m.parameters[w.parameter]
      if (m.id !== w.machine_id || !p) return m
      const last = { values: w.values, levels: w.levels, status: w.status, start: w.start }
      const parameters = { ...m.parameters, [w.parameter]: { ...p, status: w.status, last } }
      return { ...m, parameters, status: worst(parameters) }
    }),
  }
}

export function useOverview() {
  const [data, setData] = useState(null)
  const [connected, setConnected] = useState(live.connected)

  useEffect(() => {
    let alive = true
    get('/api/overview').then((d) => alive && setData(d)).catch(() => {})
    const onOverview = (d) => setData(d)
    const onReading = (r) => setData((d) => (d ? patchReading(d, r) : d))
    const onStatus = (w) => setData((d) => (d ? patchStatus(d, w) : d))
    const onConnect = () => setConnected(true)
    const onDisconnect = () => setConnected(false)
    live.on('overview', onOverview)
    live.on('reading', onReading)
    live.on('status', onStatus)
    live.on('connect', onConnect)
    live.on('disconnect', onDisconnect)
    return () => {
      alive = false
      live.off('overview', onOverview)
      live.off('reading', onReading)
      live.off('status', onStatus)
      live.off('connect', onConnect)
      live.off('disconnect', onDisconnect)
    }
  }, [])

  return { data, connected }
}
