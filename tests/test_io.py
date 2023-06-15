import pytest

@pytest.fixture
def documents(weaviate_client):
    docs = [
        {"text": "The lion is the king of the jungle"},
    ]

    for doc in docs:
        client.post("/add_vector", json=doc)

