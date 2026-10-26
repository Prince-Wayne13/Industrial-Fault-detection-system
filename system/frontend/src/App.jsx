import { Routes, Route, useLocation } from 'react-router-dom'
import TopBar from './TopBar.jsx'
import SignIn from './SignIn.jsx'
import Overview from './Overview.jsx'
import MachinesList from './MachinesList.jsx'
import MachineDetail from './MachineDetail.jsx'
import Settings from './Settings.jsx'
import Admin from './Admin.jsx'
import DemoPanel from './DemoPanel.jsx'
import Tracker from './Tracker.jsx'

export default function App() {
  const onSignIn = useLocation().pathname === '/signin'
  return (
    <>
      {!onSignIn && <TopBar />}
      <Routes>
        <Route path="/signin" element={<SignIn />} />
        <Route path="/" element={<Overview />} />
        <Route path="/machines" element={<MachinesList />} />
        <Route path="/machine/:id" element={<MachineDetail />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/demo" element={<DemoPanel />} />
        <Route path="/tracker" element={<Tracker />} />
      </Routes>
    </>
  )
}
