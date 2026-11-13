from fastapi.testclient import TestClient

from example_model.serve import LatestScores, create_app


def test_lookup_serves_latest_batch(frame):
    batch = frame[["entity_id"]].copy()
    batch["score"] = 0.42
    batch["model_version"] = "7"
    loads = []

    def load():
        loads.append(1)
        return batch.copy()

    client = TestClient(create_app(LatestScores(load, ttl_seconds=3600).get))
    assert client.get("/healthz").json() == {"status": "ok"}
    response = client.get("/predictions/5")
    assert response.status_code == 200
    assert response.json()["score"] == 0.42
    assert response.json()["model_version"] == "7"
    assert client.get("/predictions/not-an-entity").status_code == 404
    assert len(loads) == 1  # one read for all three requests


def test_cache_rereads_after_ttl(frame):
    batch = frame[["entity_id"]].head(3).copy()
    batch["score"] = 0.1
    loads = []

    def load():
        loads.append(1)
        return batch.copy()

    cache = LatestScores(load, ttl_seconds=0)
    cache.get("0")
    cache.get("0")
    assert len(loads) == 2
