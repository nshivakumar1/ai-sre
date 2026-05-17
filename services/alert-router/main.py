from fastapi import FastAPI, Request
import logging
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Alert Router")

AI_RCA_ENGINE_URL = "http://ai-rca-engine:8000"

@app.post("/webhook")
async def receive_alert(request: Request):
    payload = await request.json()
    logger.info(f"Received alert from Alertmanager: {payload}")
    
    # Simple logic: If it's a firing alert, forward it to the AI RCA Engine
    if payload.get("status") == "firing":
        alerts = payload.get("alerts", [])
        for alert in alerts:
            logger.info(f"Forwarding alert to AI RCA Engine: {alert.get('labels', {}).get('alertname')}")
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{AI_RCA_ENGINE_URL}/analyze",
                        json={"alert": alert}
                    )
                    logger.info(f"AI RCA Engine response: {response.status_code}")
            except Exception as e:
                logger.error(f"Error forwarding to AI RCA Engine: {e}")
                
    return {"status": "received"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
