// The top bar on every page: search, connection icons, bell, and the person. See design/top-bar.md.
import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Icon from './Icons.jsx'
import BellList from './BellList.jsx'
import ConnectionIcons from './ConnectionIcons.jsx'
import NamePanel from './NamePanel.jsx'
import { initials } from './format.js'
import { useUser } from './user.jsx'

export default function TopBar({ bell, storageAlerts, machines, mode, link }) {
  const { user } = useUser()
  const [open, setOpen] = useState(null)        // 'bell' | 'name' | null
  const [search, setSearch] = useState('')
  const [found, setFound] = useState(true)
  const bar = useRef(null)
  const navigate = useNavigate()
  const count = bell.length + (storageAlerts ? 1 : 0)

  useEffect(() => {
    const off = (e) => { if (e.key === 'Escape') setOpen(null) }
    const away = (e) => { if (open === 'bell' && bar.current && !bar.current.querySelector('.anchor.open')?.contains(e.target)) setOpen(null) }
    document.addEventListener('keydown', off)
    document.addEventListener('mousedown', away)
    return () => { document.removeEventListener('keydown', off); document.removeEventListener('mousedown', away) }
  }, [open])

  const find = (e) => {
    if (e.key !== 'Enter' || !search.trim()) return
    const hit = machines.find((m) => m.name.toLowerCase().includes(search.trim().toLowerCase()))
    setFound(!!hit)
    if (hit) { navigate(`/machine/${hit.id}`); setSearch('') }
  }

  return (
    <header className="topbar" ref={bar}>
      <div className="search">
        <Icon name="search" size={18} />
        <input type="search" placeholder="Search machines" aria-label="Search machines" value={search} aria-invalid={!found}
               title={found ? '' : 'No machine with that name'} onChange={(e) => { setSearch(e.target.value); setFound(true) }} onKeyDown={find} />
      </div>
      <div className="topbar-space" />
      <ConnectionIcons mode={mode} link={link} />
      <div className={`anchor${open === 'bell' ? ' open' : ''}`}>
        <button className="icon-btn" aria-label={`Faults, ${count} waiting`} aria-expanded={open === 'bell'} onClick={() => setOpen(open === 'bell' ? null : 'bell')}>
          <Icon name="bell" />
          {count > 0 && <span className="bell-badge">{count}</span>}
        </button>
        {open === 'bell' && <BellList bell={bell} storageAlerts={storageAlerts} onClose={() => setOpen(null)} />}
      </div>
      <button className="person" onClick={() => setOpen('name')} aria-haspopup="dialog">
        <span className="avatar">{initials(user.full_name)}</span>
        <span className="person-text">
          <div className="person-name">{user.full_name}</div>
          <div className="person-role">{user.role}</div>
        </span>
        <Icon name="chevron" size={16} />
      </button>
      {open === 'name' && <NamePanel onClose={() => setOpen(null)} />}
    </header>
  )
}
