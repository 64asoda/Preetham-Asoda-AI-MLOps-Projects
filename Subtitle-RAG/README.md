# SubtitleRAG 🎬

A production-grade Retrieval-Augmented Generation (RAG) system for semantic search across 2.4 million movie and TV subtitle documents.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)
![LangSmith](https://img.shields.io/badge/Observability-LangSmith-purple)

## 🎯 Project Overview

SubtitleRAG enables semantic search across a massive corpus of subtitle data, returning contextually relevant dialogue snippets based on natural language queries. Unlike traditional keyword search, this system understands meaning and context.

**Example Query:** "I'll be back" → Returns scenes with similar dramatic farewell moments, not just exact matches.

### Key Metrics
- **2.4M+ documents** indexed in ChromaDB vector database
- **24GB** vector embeddings using sentence-transformers
- **Sub-second** query response time
- **Production-ready** with health checks, monitoring, and CI/CD

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SubtitleRAG Architecture                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   User Query                                                         │
│       │                                                              │
│       ▼                                                              │
│   ┌─────────────────┐                                                │
│   │   FastAPI       │ ◄─── REST API with Swagger docs               │
│   │   /api/v1/query │                                                │
│   └────────┬────────┘                                                │
│            │                                                         │
│            ▼                                                         │
│   ┌─────────────────┐                                                │
│   │ Sentence        │ ◄─── all-mpnet-base-v2 (768-dim embeddings)   │
│   │ Transformers    │                                                │
│   └────────┬────────┘                                                │
│            │                                                         │
│            ▼                                                         │
│   ┌─────────────────┐                                                │
│   │   ChromaDB      │ ◄─── 2.4M vectors, 24GB persistent storage    │
│   │   Vector Store  │                                                │
│   └────────┬────────┘                                                │
│            │                                                         │
│            ▼                                                         │
│   ┌─────────────────┐                                                │
│   │   LangSmith     │ ◄─── Observability: latency, traces, errors   │
│   │   Monitoring    │                                                │
│   └─────────────────┘                                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **API Framework** | FastAPI | High-performance async REST API |
| **Embeddings** | sentence-transformers | all-mpnet-base-v2 model |
| **Vector Database** | ChromaDB | Persistent vector storage |
| **Containerization** | Docker | Reproducible deployments |
| **Orchestration** | Kubernetes (Minikube) | Container orchestration |
| **CI/CD** | GitHub Actions | Automated testing & deployment |
| **Monitoring** | LangSmith | LLM observability & tracing |
| **Registry** | Docker Hub | Container image storage |

---

## 📓 Data Pipeline

The embedding pipeline is documented in [`notebooks/01_build_embeddings.ipynb`](notebooks/01_build_embeddings.ipynb).

### Pipeline Overview

```
Raw Subtitles (CSV)     Chunking & Cleaning     Embedding Generation     ChromaDB Storage
    89K files      →      2.4M chunks       →     768-dim vectors    →     24GB database
```

### Key Steps

1. **Data Collection**: 89K subtitle files from OpenSubtitles dataset
2. **Text Processing**: Chunking, deduplication, cleaning
3. **Embedding Generation**: sentence-transformers/all-mpnet-base-v2
4. **Vector Storage**: Batch insertion into ChromaDB with metadata

### Data Pipeline Metrics

| Metric | Value |
|--------|-------|
| Source files | 89,000+ |
| Final chunks | 2,469,209 |
| Embedding dimensions | 768 |
| Total storage | 24 GB |

---

## 📁 Project Structure

```
Subtitle-RAG/
├── notebooks/
│   └── 01_build_embeddings.ipynb  # ChromaDB ingestion pipeline
├── src/
│   ├── api/
│   │   ├── main.py                # FastAPI application & lifespan
│   │   ├── routes.py              # API endpoint definitions
│   │   └── schemas.py             # Pydantic request/response models
│   ├── retrieval/
│   │   └── search.py              # ChromaDB search with LangSmith tracing
│   ├── embedding/
│   │   └── embedder.py            # Sentence transformer embeddings
│   └── config.py                  # Environment configuration
├── k8s/
│   ├── deployment.yaml            # Kubernetes deployment with probes
│   ├── service.yaml               # ClusterIP & NodePort services
│   ├── configmap.yaml             # Environment configuration
│   ├── pvc.yaml                   # Persistent volume for ChromaDB
│   ├── hpa.yaml                   # Horizontal Pod Autoscaler
│   └── ingress.yaml               # NGINX ingress configuration
├── tests/
│   ├── test_api.py                # API endpoint tests
│   └── conftest.py                # Pytest configuration
├── .github/workflows/
│   └── ci-cd.yml                  # GitHub Actions pipeline
├── Dockerfile                     # Multi-stage container build
├── requirements.txt               # Python dependencies
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker Desktop
- Minikube (for Kubernetes deployment)

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/subtitle-rag.git
cd subtitle-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-base.txt
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your LANGCHAIN_API_KEY

# Run application
python -m src.api.main
```

Access API documentation at: http://localhost:8000/docs

### Docker Deployment

```bash
# Build image
docker build -t subtitlerag:latest .

# Run with ChromaDB volume mounted
docker run -p 8000:8000 \
  -v /path/to/chroma_data:/app/chroma_data \
  -e LANGCHAIN_API_KEY=your_key \
  subtitlerag:latest
```

### Kubernetes Deployment (Minikube)

```bash
# Start Minikube
minikube start --memory=8192 --cpus=4

# Load image
minikube image load subtitlerag:latest

# Deploy
kubectl apply -f k8s/

# Access service
minikube service subtitle-rag-service
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/query` | Search with full options |
| `GET` | `/api/v1/search` | Simple search (query params) |
| `GET` | `/api/v1/health` | Health check (readiness probe) |
| `GET` | `/api/v1/live` | Liveness probe |
| `GET` | `/api/v1/stats` | Collection statistics |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "I love you", "top_k": 5}'
```

### Example Response

```json
{
  "query": "I love you",
  "results": [
    {
      "content": "I love you more than anything in this world.",
      "metadata": {
        "movie": "The Notebook",
        "timestamp": "01:23:45"
      },
      "similarity_score": 0.9234
    }
  ],
  "total_results": 5
}
```

---

## 🔄 CI/CD Pipeline

Automated pipeline triggered on every push to `main`:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Lint &    │───►│    Unit     │───►│  Build &    │───►│  Deployment │
│   Format    │    │    Tests    │    │  Push Docker│    │   Summary   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     19s              1m 39s             4m 18s              3s
```

### Pipeline Stages

1. **Lint & Format**: flake8, black, mypy
2. **Unit Tests**: pytest with coverage
3. **Build & Push**: Docker image to Docker Hub
4. **Summary**: Deployment instructions

---

## 📊 Observability with LangSmith

LangSmith provides production monitoring for the RAG pipeline:

### Tracked Metrics
- **Query latency**: Time from request to response
- **Retrieval traces**: Full input/output for each search
- **Error rates**: Failed queries and exceptions
- **Token usage**: Embedding token consumption

### Dashboard Features
- Real-time query monitoring
- Latency percentiles (p50, p95, p99)
- Error aggregation and alerting
- Query replay for debugging

---

## ⚙️ Kubernetes Configuration

### Resource Management

```yaml
resources:
  requests:
    memory: "4Gi"
    cpu: "1000m"
  limits:
    memory: "6Gi"
    cpu: "2000m"
```

### Health Probes

| Probe | Endpoint | Purpose |
|-------|----------|---------|
| Startup | `/api/v1/health` | Allow 15min for ChromaDB loading |
| Liveness | `/api/v1/live` | Restart if unresponsive |
| Readiness | `/api/v1/health` | Remove from traffic if unhealthy |

### Horizontal Pod Autoscaler

```yaml
minReplicas: 1
maxReplicas: 5
metrics:
  - cpu: 70%
  - memory: 80%
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_api.py::TestSchemas -v
```

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Documents indexed | 2,469,209 |
| Vector dimensions | 768 |
| Database size | 24 GB |
| Average query latency | ~200ms |
| Startup time (cold) | ~30s |

---

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHROMA_PERSIST_DIR` | ChromaDB storage path | `./chroma_data/...` |
| `EMBEDDING_MODEL` | Sentence transformer model | `all-mpnet-base-v2` |
| `API_HOST` | API bind address | `0.0.0.0` |
| `API_PORT` | API port | `8000` |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith | `true` |
| `LANGCHAIN_API_KEY` | LangSmith API key | - |
| `LANGCHAIN_PROJECT` | LangSmith project name | `SubtitleRAG` |

---

## 🚧 Future Enhancements

- [ ] Add re-ranking with cross-encoder
- [ ] Implement caching layer (Redis)
- [ ] Add authentication (JWT)
- [ ] Deploy to cloud Kubernetes (EKS/GKE)
- [ ] Add Prometheus metrics endpoint
- [ ] Implement A/B testing for retrieval strategies

---

## 📚 Lessons Learned

### MLOps Best Practices Applied

1. **Separation of concerns**: Code in image, data mounted at runtime
2. **Health probes**: Startup/liveness/readiness for Kubernetes
3. **Observability**: LangSmith tracing for RAG-specific monitoring
4. **CI/CD**: Automated testing and deployment pipeline
5. **Resource management**: Memory limits to prevent OOM in containers

### Challenges Overcome

- **Large dataset handling**: 24GB ChromaDB with 2.4M documents
- **Memory optimization**: Replaced `.get()` with `.count()` to avoid loading all IDs
- **Container startup**: Extended startup probe for model loading time

---

## 👤 Author

Preetham Asoda
- LinkedIn: https://www.linkedin.com/in/preetham-asoda/
- GitHub: https://github.com/64asoda/Preetham-Asoda-AI-MLOps-Projects

---

## 📄 License

This project is for portfolio/educational purposes.

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the RAG framework
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [LangSmith](https://smith.langchain.com/) for observability
