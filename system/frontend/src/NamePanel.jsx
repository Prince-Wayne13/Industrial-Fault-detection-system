// The panel that slides in from the right when the name is clicked: full name, role, Settings, Sign out.
import { Link } from 'react-router-dom'
import Icon from './Icons.jsx'
import Pill from './Pill.jsx'
import { useUser } from './user.jsx'
import { initials } from './format.js'

export default function NamePanel({ onClose }) {
  const { user, signOut } = useUser()
  return (
    <>
      <div className="scrim" onClick={onClose} />
      <aside className="panel" role="dialog" aria-label="Your account">
        <button className="icon-btn close" onClick={onClose} aria-label="Close"><Icon name="close" /></button>
        <div className="avatar">{initials(user.full_name)}</div>
        <h2>{user.full_name}</h2>
        <Pill level="role">{user.role}</Pill>
        <Link to="/settings" className="btn btn-quiet" onClick={onClose}><Icon name="sliders" /> Settings</Link>
        <button className="btn btn-quiet" onClick={signOut}><Icon name="logout" /> Sign out</button>
      </aside>
    </>
  )
}
