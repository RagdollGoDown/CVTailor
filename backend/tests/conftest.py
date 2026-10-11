import pytest
from fastapi.testclient import TestClient

from app.llm import get_llm
from app.llm.dummy import DummyProvider
from app.main import app


@pytest.fixture
def llm() -> DummyProvider:
    return DummyProvider()


@pytest.fixture
def client(llm: DummyProvider):
    app.dependency_overrides[get_llm] = lambda: llm
    yield TestClient(app)
    app.dependency_overrides.clear()
