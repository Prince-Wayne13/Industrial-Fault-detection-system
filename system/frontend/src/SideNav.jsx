// The left navigation. Each role sees only its own pages (see design/page-map.md).
import { NavLink } from 'react-router-dom'
import Icon from './Icons.jsx'
import { useUser } from './user.jsx'

const LINKS = [
  { to: '/', label: 'Overview', icon: 'grid', roles: ['operator', 'engineer', 'administrator'] },
  { to: '/machines', label: 'Machines', icon: 'list', roles: ['operator', 'engineer'] },
  { to: '/admin', label: 'Admin', icon: 'shield', roles: ['administrator'] },
  { to: '/logs', label: 'Logs', icon: 'log', roles: ['administrator'] },
  { to: '/settings', label: 'Settings', icon: 'sliders', roles: ['operator', 'engineer', 'administrator'] },
]
const DEMO = [
  { to: '/demo', label: 'Demo panel', icon: 'play' },
  { to: '/tracker', label: 'Tracker', icon: 'check' },
]

function Item({ to, label, icon }) {
  return (
    <NavLink to={to} end={to === '/'} className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`} title={label}>
      <Icon name={icon} />
      <span>{label}</span>
    </NavLink>
  )
}

export default function SideNav() {
  const { user } = useUser()
  const role = user.role
  return (
    <nav className="sidenav" aria-label="Main">
      <NavLink to="/" className="brand">
        <span className="brand-mark"><Icon name="mark" size={22} /></span>
        <span className="brand-text">Fault-Detect</span>
      </NavLink>
      {LINKS.filter((l) => l.roles.includes(role)).map((l) => <Item key={l.to} {...l} />)}
      <div className="nav-spacer" />
      <div className="nav-group">Demonstration</div>
      {DEMO.map((l) => <Item key={l.to} {...l} />)}
    </nav>
  )
}
