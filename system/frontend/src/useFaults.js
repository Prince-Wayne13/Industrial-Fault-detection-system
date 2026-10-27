// The faults that matter to the person acting: pop-ups (not acknowledged yet) and the bell list (acknowledged, not resolved).
import { useCallback, useEffect, useState } from 'react'
import { get, live } from './api.js'

export function useFaults(username) {
  const [state, setState] = useState({ popups: [], bell: [], storage_alerts: 0 })
  const reload = useCallback(() => {
    if (!username) return
    get(`/api/faults?user=${username}`).then((d) => d.popups && setState(d)).catch(() => {})
  }, [username])
  useEffect(() => {
    reload()
    live.on('faults_changed', reload)
    live.on('connect', reload)
    return () => { live.off('faults_changed', reload); live.off('connect', reload) }
  }, [reload])
  return { ...state, reload }
}
