import React, { useState } from 'react';
import { config } from '../config';

export default function IncidentHub({ onRcaComplete }) {
  const [loading, setLoading] = useState(false);
  const [chaosLoading, setChaosLoading] = useState(false);
  const [rcaResult, setRcaResult] = useState(null);
  const [error, setError] = useState(null);

  // Default mock alert for RCA if no live incident is triggered
  const [activeAlert, setActiveAlert] = useState({
    alerts: [
      {
        labels: { alertname: "HighCPUUsage", severity: "critical", instance: "web-server-01" },
        annotations: { description: "CPU usage is above 90% for 5 minutes." }
      }
    ]
  });

  const simulateChaos = async () => {
    setChaosLoading(true);
    setError(null);
    try {
      const liveAlert = {
        alerts: [
          {
            labels: { alertname: "DatabaseLatencySpike", severity: "critical", instance: "db-cluster-eu" },
            annotations: { description: "Query latency exceeded 2000ms threshold." }
          }
        ]
      };
      
      const response = await fetch(config.ALERT_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(liveAlert)
      });
      
      if (!response.ok) throw new Error(`Alert Router failed: ${response.status}`);
      
      setActiveAlert(liveAlert);
    } catch (err) {
      console.error(err);
      setError("Failed to simulate chaos. Ensure alert-router is reachable.");
    } finally {
      setChaosLoading(false);
    }
  };

  const triggerRCA = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(config.RCA_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(activeAlert)
      });
      if (!response.ok) throw new Error(`RCA Engine failed: ${response.status}`);
      
      const data = await response.json();
      setRcaResult(data);
      if (onRcaComplete) onRcaComplete(data);
    } catch (err) {
      console.error(err);
      setError("RCA Analysis failed. Ensure backend services are reachable.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="component-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3>Incident Hub</h3>
        <button className="btn-danger" onClick={simulateChaos} disabled={chaosLoading}>
          {chaosLoading ? 'Injecting Fault...' : '⚡ Simulate Live Chaos'}
        </button>
      </div>

      <div className="alert-card" style={{ marginTop: '1rem' }}>
        <span className="badge critical">CRITICAL</span>
        <h4>{activeAlert.alerts[0].labels.alertname} on {activeAlert.alerts[0].labels.instance}</h4>
        <p style={{ color: '#aaa', fontSize: '0.9rem', marginBottom: '1rem' }}>{activeAlert.alerts[0].annotations.description}</p>
        <button className="btn-primary" onClick={triggerRCA} disabled={loading}>
          {loading ? 'Analyzing...' : 'Run AI Root Cause Analysis'}
        </button>
      </div>
      
      {error && <div className="status-banner warning" style={{ marginTop: '1rem' }}>{error}</div>}

      {rcaResult && (
        <div className="rca-result">
          <h4>RCA Results</h4>
          <p><strong>Incident:</strong> {rcaResult.incident}</p>
          <p><strong>Probable Cause:</strong> {rcaResult.probable_cause}</p>
          <p><strong>Recommended Fix:</strong> {rcaResult.recommended_fix}</p>
          <span className="badge info">Confidence: {rcaResult.confidence_score}</span>
        </div>
      )}
    </div>
  );
}
