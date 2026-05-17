import React, { useState } from 'react';

export default function DriftDashboard() {
  const [loading, setLoading] = useState(false);
  const [driftResult, setDriftResult] = useState(null);

  const detectDrift = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8005/detect');
      const data = await response.json();
      setDriftResult(data);
    } catch (err) {
      console.error(err);
      setDriftResult({ status: 'error', message: 'Failed to connect to Drift Detector API' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="component-container">
      <h3>Infrastructure Drift Detector</h3>
      <p>Scan for configuration drift between Terraform state and Azure.</p>
      <button className="btn-secondary" onClick={detectDrift} disabled={loading}>
        {loading ? 'Scanning...' : 'Run Drift Detection'}
      </button>
      
      {driftResult && (
        <div className={`status-banner ${driftResult.drift_detected ? 'warning' : 'success'}`}>
          {driftResult.message}
        </div>
      )}
    </div>
  );
}
