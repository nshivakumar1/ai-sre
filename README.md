# 🚀 AI-SRE Copilot Platform

An autonomous incident management and observability platform designed to automatically ingest infrastructure alerts, perform Root Cause Analysis (RCA) using Large Language Models (LLMs), and suggest actionable remediation steps via a localized RAG knowledge base.

![Platform Dashboard](./docs/architecture/dashboard-preview.png) *(Note: Ensure UI is running to view the premium dark-mode glassmorphism dashboard!)*

## 🧠 Core Architecture

The platform is divided into 5 independent microservices, orchestrated via Docker and deployable to Azure Container Apps:

1. **SRE Copilot UI** (`React + Vite`): A premium dark-mode glassmorphism dashboard providing a unified view of alerts, RCA data, and chat interfaces.
2. **Alert Router** (`FastAPI`): Ingests webhooks from Prometheus Alertmanager, normalizes the payloads, and routes them to the RCA engine.
3. **AI RCA Engine** (`FastAPI + Google Gemini`): Processes normalized incidents and prompts Gemini Pro to generate incident summaries and root-cause hypotheses.
4. **Incident Summarizer** (`FastAPI + LangChain`): Auxiliary LangChain API for complex incident narrative generation.
5. **Chatbot API** (`FastAPI + OpenAI + ChromaDB`): Powers the conversational interface. Connects a LangChain Agent to live observability data and queries an embedded Vector Database (ChromaDB) for localized SRE Runbook context via RAG.

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Pydantic
- **Frontend**: React, Vite, TailwindCSS (Vanilla CSS Glassmorphism)
- **AI & Data**: LangChain, OpenAI GPT-4o, Google Gemini Pro, ChromaDB, FAISS
- **Observability**: Prometheus, Alertmanager, Grafana, Loki, Promtail
- **Infrastructure**: Docker Compose, Terraform, Azure Container Apps (ACA), GitHub Actions

## 🚀 Getting Started (Local Development)

### 1. Prerequisites
- Docker & Docker Compose
- API Keys for OpenAI, Gemini, and LangChain

### 2. Environment Setup
Create a `.env` file in the root directory (based on `.env.example` if applicable) and populate your keys:
```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
LANGCHAIN_API_KEY=your_langchain_key
```

### 3. Run Locally
We have provided a convenience script to build and launch the entire stack:
```bash
chmod +x scripts/deploy_local.sh
./scripts/deploy_local.sh
```
- **SRE Copilot UI**: [http://localhost:3002](http://localhost:3002)
- **Grafana Dashboard**: [http://localhost:3000](http://localhost:3000)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)

### 4. Simulating an Incident
To test the AI RCA pipeline locally, run the simulation script to fire a mock webhook to the Alert Router:
```bash
./scripts/simulate_incident.sh
```

## ☁️ Cloud Deployment (Azure)

This project is fully equipped with Terraform modules and GitHub Actions for a GitOps deployment to Azure Container Apps.

1. **Base Infrastructure**: Run `terraform apply` inside `infra/terraform` to provision the Virtual Network, Log Analytics Workspace, Azure Key Vault, and the Container App Environment.
2. **GitHub Secrets**: Add the following secrets to your GitHub Repository:
   - `AZURE_CREDENTIALS` (Service Principal JSON)
   - `OPENAI_API_KEY`, `GEMINI_API_KEY`, `LANGCHAIN_API_KEY`
3. **Deploy**: Push your code to the `main` branch. The `.github/workflows/ci-cd.yml` pipeline will automatically build the Docker images, push them to `ghcr.io`, and deploy them to your Azure environment!

## 📚 Documentation
- View the detailed [System Architecture](./docs/architecture/architecture.md).
- Internal Incident Runbooks are located in `./docs/runbooks/`.
