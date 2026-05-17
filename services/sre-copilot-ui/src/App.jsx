import { useState } from 'react'
import IncidentHub from './components/IncidentHub'
import RemediationHub from './components/RemediationHub'
import Chatbot from './components/Chatbot'
import PostmortemGenerator from './components/PostmortemGenerator'
import DriftDashboard from './components/DriftDashboard'

function App() {
  const [rcaData, setRcaData] = useState(null);

  return (
    <div className="app-container animate-fade-in">
      {/* Premium Background Orbs */}
      <div className="glow-orb orb-1"></div>
      <div className="glow-orb orb-2"></div>

      <div className="animate-fade-in delay-1">
        <header className="glass-header floating-header">
          <h1 className="gradient-text">AI SRE Copilot Platform</h1>
          <div className="status-badge pulse-healthy">System Healthy</div>
        </header>
      </div>
      
      <main className="dashboard-grid">
        <section className="glass-panel animate-fade-in delay-2">
          <IncidentHub onRcaComplete={setRcaData} />
        </section>
        
        <section className="glass-panel animate-fade-in delay-2">
          <RemediationHub rcaData={rcaData} />
        </section>

        <section className="glass-panel chat-panel animate-fade-in delay-3">
          <h2>Copilot Chat</h2>
          <Chatbot />
        </section>

        <section className="glass-panel animate-fade-in delay-4">
          <PostmortemGenerator />
          <hr className="divider" />
          <DriftDashboard />
        </section>
      </main>
    </div>
  )
}

export default App
