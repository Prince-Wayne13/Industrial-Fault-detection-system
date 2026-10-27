import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import BellList from './BellList.jsx'
import { useUser } from './user.jsx'

// Shared top bar: name, search, bell, person. See docs/design/top-bar.md
export default function TopBar({ bell, storageAlerts, machines, mode, link }) {
  const [bellOpen, setBellOpen] = useState(false)
  const [sideOpen, setSideOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [found, setFound] = useState(true)
  const { user, signOut } = useUser()
  const navigate = useNavigate()
  const count = bell.length + (storageAlerts ? 1 : 0)
  const role = user.role

  const find = (e) => {
    if (e.key !== 'Enter' || !search.trim()) return
    const hit = machines.find((m) => m.name.toLowerCase().includes(search.trim().toLowerCase()))
    setFound(!!hit)
    if (hit) { navigate(`/machine/${hit.id}`); setSearch('') }
  }

  return (
    <div className="topbar">
      <Link to="/" className="brand">Fault-Detect</Link>
      <input placeholder="Search machines" value={search} aria-invalid={!found} title={found ? '' : 'No machine with that name'}
             onChange={(e) => { setSearch(e.target.value); setFound(true) }} onKeyDown={find} />
      {role !== 'administrator' && <Link to="/machines" className="navlink first">Machines</Link>}
      {role === 'administrator' && <Link to="/admin" className="navlink first">Admin</Link>}
      <Link to="/demo" className="navlink">Demo</Link>
      <Link to="/tracker" className="navlink">Tracker</Link>
      {mode && <span className="chip" title="Connection mode">{mode === 'near' ? 'Near range · Bluetooth' : 'Remote range · Wi-Fi'}{link === 'cut' && ' · cut'}</span>}
      <div className="bell-wrap">
        <button onClick={() => setBellOpen(!bellOpen)} aria-label={`Bell, ${count} open`}>Bell {count > 0 && <span className="bell-count">{count}</span>}</button>
        {bellOpen && <BellList bell={bell} storageAlerts={storageAlerts} onClose={() => setBellOpen(false)} />}
      </div>
      <button onClick={() => setSideOpen(true)}>{user.full_name}</button>
      {sideOpen && (
        <>
          <div className="side-backdrop" onClick={() => setSideOpen(false)} />
          <aside className="sidebar">
            <h3>{user.full_name}</h3>
            <p className="muted" style={{ textTransform: 'capitalize' }}>{role}</p>
            <Link to="/settings" onClick={() => setSideOpen(false)}>Settings</Link>
            <button className="demo-btn" onClick={signOut}>Sign out</button>
          </aside>
        </>
      )}
    </div>
  )
}
