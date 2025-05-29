# LLM-InfraLite

A Lightweight Serving System for Open LLMs

## 🎯 Project Overview

LLM-InfraLite is a lightweight infrastructure demo for LLM applications, designed to showcase platform engineering capabilities and AI understanding. The project aims to build a production-ready LLM inference system with features like model serving, monitoring, and auto-scaling.

## 🚀 Key Features

- Model Serving: Deploy LLaMA2 or Mistral models using FastChat/vLLM
- RESTful API: Support both synchronous and streaming inference
- Multi-Model Management: Hot-swap between different model versions
- Monitoring: Prometheus + Grafana for throughput, latency, and GPU metrics
- Observability: Structured logging + OpenTelemetry for full-chain tracing
- Auto-scaling: Kubernetes HPA or custom scaling strategies
- Optional Features:
  - Management Dashboard: Model status and control panel
  - Client SDK: Python SDK for easy integration

## 🛠 Tech Stack

- Language: Python (core services), Shell (deployment scripts)
- Model Inference: vLLM or FastChat
- Framework: FastAPI + Uvicorn
- Containerization: Docker + Kubernetes
- Configuration: Helm/Kustomize
- Monitoring: Prometheus/Grafana
- CI/CD: GitHub Actions/Argo Workflows (optional)

## 📦 Project Structure

```
llm-infralite/
├── api/                  # FastAPI service
├── k8s/                  # Kubernetes configurations
├── monitoring/           # Monitoring setup
└── docs/                 # Documentation
```

## 📝 Documentation

For detailed architecture and implementation details, please check the [documentation](doc/infraLite-arch.md).

## 🌟 Development Roadmap

1. Week 1: Basic System Setup
   - Model deployment with vLLM/FastChat
   - Basic FastAPI interface
   - Docker containerization
   - Basic documentation

2. Week 2: Enhanced Features + Monitoring
   - Multi-model switching
   - Prometheus integration
   - Structured logging and tracing

3. Week 3: Kubernetes Deployment
   - Helm/Kustomize configuration
   - Auto-scaling setup
   - Load balancing

4. Week 4: Project Polish
   - Documentation enhancement
   - Performance optimization
   - Demo preparation

## 📄 License

MIT License