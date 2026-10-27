import { Navigate, Routes, Route } from 'react-router-dom'
import Layout from './Layout.jsx'
import SignIn from './SignIn.jsx'
import Overview from './Overview.jsx'
import MachinesList from './MachinesList.jsx'
import MachineDetail from './MachineDetail.jsx'
import Settings from './Settings.jsx'
import Admin from './Admin.jsx'
import Logs from './Logs.jsx'
import DemoPanel from './DemoPanel.jsx'
import Tracker from './Tracker.jsx'
import { UserProvider, useUser } from './user.jsx'
import { useFaults } from './useFaults.js'
import { useOverview } from './useLive.js'

// FR-27: a role that may not use a page is turned away here. The server checks the role as well.
function Require({ roles, children }) {
  const { user } = useUser()
  if (roles.includes(user.role)) return children
  return <div className="page"><h1>Not allowed</h1><p className="muted">Your role ({user.role}) cannot open this page.</p></div>
}

function Signed() {
  const { user } = useUser()
  const faults = useFaults(user.username)
  const { data } = useOverview()
  const machineType = (id) => data?.machines.find((m) => m.id === id)?.type
  return (
    <Layout faults={faults} overview={data} machineType={machineType}>
      <Routes>
        <Route path="/signin" element={<Navigate to="/" replace />} />
        <Route path="/" element={<Overview />} />
        <Route path="/machines" element={<Require roles={['operator', 'engineer']}><MachinesList /></Require>} />
        <Route path="/machine/:id" element={<MachineDetail />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/admin" element={<Require roles={['administrator']}><Admin /></Require>} />
        <Route path="/logs" element={<Require roles={['administrator']}><Logs /></Require>} />
        <Route path="/demo" element={<DemoPanel />} />
        <Route path="/tracker" element={<Tracker />} />
      </Routes>
    </Layout>
  )
}

function Shell() {
  const { user, ready } = useUser()
  if (!ready) return null
  return (
    <Routes>
      <Route path="/signin" element={user ? <Navigate to="/" replace /> : <SignIn />} />
      <Route path="*" element={user ? <Signed /> : <Navigate to="/signin" replace />} />
    </Routes>
  )
}

export default function App() {
  return <UserProvider><Shell /></UserProvider>
}
