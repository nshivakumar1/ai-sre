from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Terraform Drift Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/detect")
async def detect_drift():
    logger.info("Starting drift detection run")
    # In a real environment, this would:
    # 1. Pull the latest Terraform state file from Azure Blob Storage.
    # 2. Run `terraform plan` against the current infrastructure.
    # 3. If there is a diff, pass it to an LLM to explain the drift.
    
    return {
        "status": "completed",
        "drift_detected": False,
        "message": "Simulated run. No drift detected."
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
