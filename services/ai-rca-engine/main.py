from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI RCA Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use a default API key or grab from env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dummy-key-for-local-dev")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini") # Using a small fast model by default

class AlertPayload(BaseModel):
    alert: dict

@app.post("/analyze")
async def analyze_incident(payload: AlertPayload):
    alert = payload.alert
    alert_name = alert.get("labels", {}).get("alertname", "Unknown Alert")
    labels = alert.get("labels", {})
    annotations = alert.get("annotations", {})
    
    logger.info(f"Starting RCA analysis for alert: {alert_name}")
    
    # In a real environment, we would also query Prometheus and Loki here
    # to append recent metrics and logs to the prompt.
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert SRE engineer analyzing monitoring alerts. Return ONLY a valid JSON object with the following keys: probable_cause, severity, impacted_systems, recommended_fix, confidence_score."),
        ("user", "Alert Name: {alert_name}\nLabels: {labels}\nAnnotations: {annotations}\n\nAnalyze this alert and provide a JSON response.")
    ])
    
    # We initialize the LLM
    llm = ChatOpenAI(
        model=MODEL_NAME, 
        temperature=0.2, 
        api_key=OPENAI_API_KEY
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        if OPENAI_API_KEY == "dummy-key-for-local-dev":
            # Mock response if no key is provided
            logger.warning("No OPENAI_API_KEY provided. Returning mock RCA data.")
            analysis_result = {
                "incident": alert_name,
                "probable_cause": "Simulated cause due to missing API key",
                "severity": "high",
                "impacted_systems": ["mock-system"],
                "recommended_fix": "Provide OPENAI_API_KEY to ai-rca-engine",
                "confidence_score": "10%"
            }
        else:
            response_text = chain.invoke({
                "alert_name": alert_name,
                "labels": json.dumps(labels),
                "annotations": json.dumps(annotations)
            })
            
            # Clean up potential markdown formatting in response
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            analysis_result = json.loads(response_text)
            analysis_result["incident"] = alert_name
            
    except Exception as e:
        logger.error(f"Error during LLM analysis: {e}")
        analysis_result = {
            "incident": alert_name,
            "probable_cause": "Error during analysis",
            "severity": "unknown",
            "impacted_systems": [],
            "recommended_fix": f"Check AI Engine logs. Error: {str(e)}",
            "confidence_score": "0%"
        }
        
    logger.info(f"RCA Result: {analysis_result}")
    
    # Here we would normally forward the result to the remediation-engine
    # For now, just return it.
    
    return analysis_result

@app.get("/health")
def health_check():
    return {"status": "healthy"}
