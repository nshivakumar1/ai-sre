const getBaseUrl = (serviceName, localPort) => {
  const hostname = window.location.hostname;
  
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return `http://localhost:${localPort}`;
  }
  
  // In Azure Container Apps, FQDN looks like: sre-copilot-ui.agreeablepebble-45923bcd.centralindia.azurecontainerapps.io
  // We dynamically swap 'sre-copilot-ui' with the target service name
  return `https://${hostname.replace('sre-copilot-ui', serviceName)}`;
};

export const config = {
  RCA_URL: `${getBaseUrl('ai-rca-engine', 8002)}/analyze`,
  REMEDIATE_URL: `${getBaseUrl('incident-summarizer', 8003)}/remediate`,
  CHATBOT_URL: `${getBaseUrl('chatbot-api', 8000)}/chat`,
  ALERT_URL: `${getBaseUrl('alert-router', 8001)}/alert`
};
