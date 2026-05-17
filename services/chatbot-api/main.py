from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
import httpx
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import tool
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SRE Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dummy-key-for-local-dev")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
PROMETHEUS_URL = "http://prometheus:9090"
RUNBOOKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs/runbooks"))

# Initialize Vector DB
logger.info("Initializing Vector DB for SRE Runbooks...")
vectorstore = None
if OPENAI_API_KEY != "dummy-key-for-local-dev" and os.path.exists(RUNBOOKS_DIR):
    try:
        docs = []
        for filename in os.listdir(RUNBOOKS_DIR):
            if filename.endswith(".md"):
                file_path = os.path.join(RUNBOOKS_DIR, filename)
                loader = TextLoader(file_path)
                docs.extend(loader.load())
                
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        split_docs = text_splitter.split_documents(docs)
        
        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        vectorstore = Chroma.from_documents(split_docs, embeddings)
        logger.info(f"Successfully ingested {len(split_docs)} runbook chunks into ChromaDB.")
    except Exception as e:
        logger.error(f"Failed to initialize ChromaDB: {e}")

class ChatRequest(BaseModel):
    query: str

@tool
def check_prometheus_alerts() -> str:
    """Checks Prometheus for any currently active or firing alerts."""
    try:
        response = httpx.get(f"{PROMETHEUS_URL}/api/v1/alerts", timeout=5.0)
        data = response.json()
        if data.get("status") == "success":
            alerts = data["data"]["alerts"]
            if not alerts:
                return "No active alerts found. The infrastructure is currently healthy."
            return f"Found {len(alerts)} active alerts: {alerts}"
        return "Failed to parse Prometheus alerts."
    except Exception as e:
        return f"Error contacting Prometheus: {str(e)}"

@tool
def check_target_health() -> str:
    """Queries Prometheus to check the UP status of all monitored targets (node-exporter, cadvisor, etc)."""
    try:
        response = httpx.get(f"{PROMETHEUS_URL}/api/v1/query?query=up", timeout=5.0)
        data = response.json()
        if data.get("status") == "success":
            results = data["data"]["result"]
            down_targets = [r for r in results if r["value"][1] == "0"]
            if not down_targets:
                return "All monitoring targets are up and healthy."
            return f"Found down targets: {down_targets}"
        return "Failed to parse Prometheus targets."
    except Exception as e:
        return f"Error contacting Prometheus: {str(e)}"

        return f"Error contacting Prometheus: {str(e)}"

@tool
def search_sre_runbooks(query: str) -> str:
    """Searches the internal SRE Runbook Knowledge Base for incident remediation and troubleshooting steps."""
    if not vectorstore:
        return "The SRE Runbook Knowledge Base is currently unavailable or not initialized."
    
    try:
        docs = vectorstore.similarity_search(query, k=2)
        if not docs:
            return "No relevant runbook entries found for your query."
        
        response_text = "Found the following runbook excerpts:\n\n"
        for i, doc in enumerate(docs):
            response_text += f"--- Excerpt {i+1} ---\n{doc.page_content}\n\n"
        return response_text
    except Exception as e:
        return f"Error searching runbooks: {str(e)}"

tools = [check_prometheus_alerts, check_target_health, search_sre_runbooks]
@app.post("/chat")
async def chat(request: ChatRequest):
    logger.info(f"Received query: {request.query}")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI Site Reliability Engineering Copilot. You have access to tools that can query the live observability stack and search internal SRE runbooks. Use the search_sre_runbooks tool to find remediation steps for incidents. Answer the user's infrastructure and incident questions professionally and concisely. If all targets are up and there are no alerts, confidently state the infrastructure is healthy."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    llm = ChatOpenAI(
        model=MODEL_NAME, 
        temperature=0.2, 
        api_key=OPENAI_API_KEY
    )
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    try:
        if OPENAI_API_KEY == "dummy-key-for-local-dev":
            response = "This is a mock response. Please configure OPENAI_API_KEY to interact with the LLM."
        else:
            result = agent_executor.invoke({"input": request.query})
            response = result["output"]
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        response = f"Error during chat: {e}"
        
    return {"reply": response}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
