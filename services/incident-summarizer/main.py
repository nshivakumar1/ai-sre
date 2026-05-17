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

app = FastAPI(title="Incident Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dummy-key-for-local-dev")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

class PostmortemPayload(BaseModel):
    incident: str
    probable_cause: str
    action_taken: str
    status: str

@app.post("/generate-postmortem")
async def generate_postmortem(payload: PostmortemPayload):
    logger.info(f"Generating postmortem for incident: {payload.incident}")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert SRE engineer. Generate a professional incident postmortem in Markdown format based on the provided details. Include Executive Summary, Timeline, Root Cause, Remediation Taken, and Preventive Actions."),
        ("user", "Incident: {incident}\nProbable Cause: {probable_cause}\nRemediation Taken: {action_taken}\nStatus: {status}\n\nPlease generate the postmortem.")
    ])
    
    llm = ChatOpenAI(
        model=MODEL_NAME, 
        temperature=0.3, 
        api_key=OPENAI_API_KEY
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        if OPENAI_API_KEY == "dummy-key-for-local-dev":
            postmortem = f"# Postmortem: {payload.incident}\n\n## Executive Summary\nA simulated incident occurred due to {payload.probable_cause}.\n\n## Remediation Taken\n{payload.action_taken} ({payload.status})"
        else:
            postmortem = chain.invoke({
                "incident": payload.incident,
                "probable_cause": payload.probable_cause,
                "action_taken": payload.action_taken,
                "status": payload.status
            })
            
    except Exception as e:
        logger.error(f"Error generating postmortem: {e}")
        postmortem = f"Error generating postmortem: {e}"
        
    return {"postmortem": postmortem}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
