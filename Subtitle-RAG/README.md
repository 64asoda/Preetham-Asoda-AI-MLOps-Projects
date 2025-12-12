# SubtitleRAG

A production-grade RAG (Retrieval-Augmented Generation) system for semantic subtitle search, built with FastAPI, LangChain, and ChromaDB.

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-blue)

## 🎯 Features

- **Semantic Search**: Find subtitles by meaning, not just keywords
- **89K+ Documents**: Pre-indexed subtitle database
- **Fast Retrieval**: Sub-second query responses with ChromaDB
- **Production Ready**: Kubernetes deployment with auto-scaling
- **Observable**: LangSmith integration for LLM monitoring

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    FastAPI      │────▶│   LangChain     │────▶│   ChromaDB      │
│   (REST API)    │     │  (Embeddings)   │     │  (Vector DB)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐                             ┌─────────────────┐
│   Kubernetes    │                             │   LangSmith     │
│  (Orchestrate)  │                             │  (Monitoring)   │
└─────────────────┘                             └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- Your saved ChromaDB embeddings (`subtitle_project_chroma_db_.zip`)

### Local Development

```bash
# Clone and setup
git clone <your-repo>
cd subtitle-rag

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Extract ChromaDB embeddings (Windows PowerShell)
Expand-Archive -Path subtitle_project_chroma_db_.zip -DestinationPath .\chroma_data

# Configure
copy .env.example .env
# Edit .env with your settings

# Run
python -m src.api.main
```

### Test the API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Search
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "I will be back", "top_k": 5}'
```

### Docker

```bash
docker build -t subtitle-rag .
docker-compose up -d
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/stats` | Collection statistics |
| POST | `/api/v1/query` | Search subtitles |
| GET | `/api/v1/search?q=...` | Simple search |

## ☸️ Kubernetes Deployment

```bash
# Start Minikube
minikube start --memory=4096 --cpus=2

# Build image
eval $(minikube docker-env)
docker build -t subtitle-rag:latest .

# Deploy
kubectl apply -f k8s/

# Access
minikube service subtitle-rag-nodeport
```

## 📊 Monitoring with LangSmith

```bash
# Set environment variables
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-api-key
export LANGCHAIN_PROJECT=subtitle-rag
```

## 🧪 Testing

```bash
pytest tests/ -v --cov=src
```

## 📁 Project Structure

```
subtitle-rag/
├── src/
│   ├── config.py              # Configuration
│   ├── api/                   # FastAPI app
│   ├── ingestion/             # Data loading
│   ├── preprocessing/         # Text cleaning
│   ├── embedding/             # Embeddings
│   └── retrieval/             # ChromaDB search
├── tests/                     # Unit tests
├── k8s/                       # Kubernetes manifests
├── .github/workflows/         # CI/CD pipeline
├── Dockerfile
└── docker-compose.yml
```

## 📄 License

MIT License
