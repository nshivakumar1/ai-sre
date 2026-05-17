import React, { useState } from 'react';

export default function PostmortemGenerator() {
  const [loading, setLoading] = useState(false);
  const [postmortem, setPostmortem] = useState(null);

  const mockIncidentData = {
    incident: "Database Connection Timeout",
    probable_cause: "High connection pool utilization due to unoptimized queries",
    action_taken: "Scaled up database connection pool and restarted service",
    status: "Resolved"
  };

  const generatePostmortem = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8004/generate-postmortem', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mockIncidentData)
      });
      const data = await response.json();
      setPostmortem(data.postmortem);
    } catch (err) {
      console.error(err);
      setPostmortem("Error generating postmortem. Check API connectivity.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="component-container">
      <h3>Postmortem Generator</h3>
      <p>Generate automated postmortems for resolved incidents.</p>
      <button className="btn-secondary" onClick={generatePostmortem} disabled={loading}>
        {loading ? 'Generating...' : 'Generate from Latest Incident'}
      </button>
      
      {postmortem && (
        <div className="postmortem-result">
          <pre>{postmortem}</pre>
        </div>
      )}
    </div>
  );
}
