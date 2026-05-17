import React, { useState } from 'react';

export default function RemediationHub({ rcaData }) {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);

  const executeRemediation = async () => {
    if (!rcaData) return;
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8003/remediate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          incident: rcaData.incident,
          probable_cause: rcaData.probable_cause,
          recommended_fix: rcaData.recommended_fix,
          confidence_score: rcaData.confidence_score
        })
      });
      const data = await response.json();
      setStatus(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="component-container">
      <h3>Remediation Action Center</h3>
      {!rcaData ? (
        <p className="placeholder-text">Run RCA first to see remediation options.</p>
      ) : (
        <div className="remediation-card">
          <p><strong>Proposed Action:</strong> {rcaData.recommended_fix}</p>
          <button className="btn-success" onClick={executeRemediation} disabled={loading}>
            {loading ? 'Executing...' : 'Approve & Execute Fix'}
          </button>
          
          {status && (
            <div className={`status-banner ${status.status.includes('success') ? 'success' : 'warning'}`}>
              Execution Status: {status.status}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
