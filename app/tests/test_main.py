import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.tests.db import engine, override_get_db
from app import main


@pytest.fixture()
def test_db():
    """
    Test database.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


main.app.dependency_overrides[get_db] = override_get_db

client = TestClient(main.app)


def test_health():
    """
    Test health route.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_payment(test_db):
    response = client.post(
        "/qrcode",
        json={
            "external_id": "10634272829",
            "value": 32.5
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "external_id": "10634272829",
        "status": "Pendente",
        "value": 32.5,
        "qrcode": "PIX+QRCODE"
    }

    with patch("httpx.post") as mock_post:
        mock_post.return_value.status_code = 201

        response = client.post(
            "/callback",
            json={"id": 1, "status": "Efetuado"}
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "status": "Efetuado",
        }


def test_callback_non_existing_payment(test_db):
    """Callback to non existing payment"""

    response = client.post(
        "/callback",
        json={"id": 1, "status": "Efetuado"}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Payment not found"
    }
