"""
Basic API tests for SubtitleRAG.
"""
import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint returns welcome message."""
        # Import here to avoid loading heavy dependencies
        from src.api.main import app
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
        assert "SubtitleRAG" in response.json()["message"]

    def test_live_endpoint(self):
        """Test liveness probe endpoint."""
        from src.api.main import app
        client = TestClient(app)
        
        response = client.get("/api/v1/live")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"


class TestSchemas:
    """Test Pydantic schemas."""

    def test_query_request_valid(self):
        """Test valid query request."""
        from src.api.schemas import QueryRequest
        
        request = QueryRequest(query="test query", top_k=5)
        assert request.query == "test query"
        assert request.top_k == 5

    def test_query_request_defaults(self):
        """Test query request default values."""
        from src.api.schemas import QueryRequest
        
        request = QueryRequest(query="test")
        assert request.top_k == 5  # default
        assert request.score_threshold is None

    def test_query_request_validation(self):
        """Test query request validation."""
        from src.api.schemas import QueryRequest
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            QueryRequest(query="", top_k=5)  # Empty query

        with pytest.raises(ValidationError):
            QueryRequest(query="test", top_k=100)  # top_k > 50