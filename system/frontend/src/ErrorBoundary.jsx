// Catches a crash on one page so the person sees a message, not a blank screen. The rest of the system keeps running.
import { Component } from 'react'
import { Link } from 'react-router-dom'

export default class ErrorBoundary extends Component {
  state = { error: null }

  static getDerivedStateFromError(error) {
    return { error }
  }

  componentDidCatch(error) {
    console.error('Page error:', error)
  }

  render() {
    if (!this.state.error) return this.props.children
    return (
      <div className="page">
        <h1>This page could not be shown</h1>
        <p className="muted">Something went wrong on this page. The rest of the system is still running and nothing was lost.</p>
        <div className="demo-row">
          <button className="demo-btn" onClick={() => this.setState({ error: null })}>Try again</button>
          <Link to="/">Back to Overview</Link>
        </div>
      </div>
    )
  }
}
