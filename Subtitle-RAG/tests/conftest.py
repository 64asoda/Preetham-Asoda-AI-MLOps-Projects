"""
Pytest configuration and fixtures.
"""
import pytest
import os

# Set test environment variables before importing app
os.environ["CHROMA_PERSIST_DIR"] = "./test_chroma_data"
os.environ["CHROMA_COLLECTION_NAME"] = "test_collection"