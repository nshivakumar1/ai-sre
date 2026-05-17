# AI-SRE Copilot Platform Architecture

## Overview
The AI-SRE Copilot is an autonomous incident management platform. It ingests monitoring data, automatically triggers root-cause analyses using Large Language Models (LLMs), searches internal runbooks using Retrieval-Augmented Generation (RAG), and provides a modern web interface for engineers to review and approve remediations.

## Core Microservices
1. **SRE Copilot UI (React + Vite)**: A premium glassmorphism dark-mode dashboard providing a unified view of alerts, RCA data, and chat interfaces.
2. **Alert Router (FastAPI)**: Ingests webhooks from Prometheus Alertmanager. Normalizes the payloads and routes them to the RCA engine.
3. **AI RCA Engine (FastAPI + Gemini)**: Processes normalized incidents. Prompts Google's Gemini Pro to generate incident summaries and root-cause hypotheses.
4. **Incident Summarizer (FastAPI + LangChain)**: An auxiliary LangChain API for complex incident narrative generation.
5. **Chatbot API (FastAPI + OpenAI + ChromaDB)**: Powers the conversational interface. Connects an Agent to live observability data (Prometheus tools) and queries an embedded Vector Database (ChromaDB) for localized SRE Runbook context.

## Observability Stack
- **Prometheus**: Scrapes metrics from target nodes and containers. Evaluates alert rules.
- **Alertmanager**: Receives firing alerts from Prometheus and forwards them to the Alert Router webhook.
- **Grafana**: Visualizes metrics on dashboards.
- **Loki & Promtail**: Centralized logging aggregation pipeline.

## Infrastructure
- **Docker Compose**: Used for local orchestration and development.
- **Azure Container Apps**: The target production runtime, provisioned via Terraform, offering serverless scaling for the microservices.
- **Azure Log Analytics**: Central telemetry sink for the Azure environment.
