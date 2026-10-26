import { Link } from 'react-router-dom'

// Shared top bar: name, search, bell, person. Step 5. See docs/design/top-bar.md
export default function TopBar() {
  return (
    <div className="topbar">
      <Link to="/" className="brand">Fault-Detect</Link>
      <input placeholder="Search machines" />
      <button>Bell</button>
      <button>Name</button>
    </div>
  )
}
