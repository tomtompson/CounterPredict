import os

import httpx
import pytest

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=BASE_URL, timeout=30) as c:
        yield c
