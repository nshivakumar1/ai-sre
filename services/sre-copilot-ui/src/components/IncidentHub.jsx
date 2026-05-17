import React, { useState } from 'react';

export default function IncidentHub({ onRcaComplete }) {
  const [loading, setLoading] = useState(false);
  const [rcaResult, setRcaResult] = useState(null);

  const mockAlert = {
    alerts: [
      {
        labels: { alertname: "HighCPUUsage", severity: "critical", instance: "web-server-01" },
        annotations: { description: "CPU usage is above 90% for 5 minutes." }
      }
    ]
  };

  const triggerRCA = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8002/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mockAlert)
      });
      const data = await response.json();
      setRcaResult(data);
      if (onRcaComplete) onRcaComplete(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="component-container">
      <h3>Incident Hub</h3>
      <div className="alert-card">
        <span className="badge critical">CRITICAL</span>
        <h4>HighCPUUsage on web-server-01</h4>
        <button className="btn-primary" onClick={triggerRCA} disabled={loading}>
          {loading ? 'Analyzing...' : 'Run AI Root Cause Analysis'}
        </button>
      </div>
      
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
