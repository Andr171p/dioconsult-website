import requests

from .constants import STATUS_CREATED, STATUS_DELETED, STATUS_OK


def get_ai_response(payload: dict) -> dict:
    response = requests.post(
        url=f"http://127.0.0.1:8000/api/v1/chat/{payload['id']}/completion",
        json=payload,
        timeout=5,
    )
    if response.status_code != STATUS_OK:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
    return response.json()


def add_document(text: str) -> list:
    response = requests.post(
        url="http://127.0.0.1:8000/api/v1/admin/documents",
        json={"text": text},
        timeout=5,
    )
    if response.status_code != STATUS_CREATED:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
    return response.json()


def upload_document(file: bytes) -> list:
    response = requests.post(
        url="http://127.0.0.1:8000/api/v1/admin/documents/upload",
        files={"file": file},
        timeout=5,
    )
    if response.status_code != STATUS_CREATED:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
    return response.json()


def delete_document(ids: list[str]) -> None:
    response = requests.delete(
        url="http://127.0.0.1:8000/api/v1/admin/documents",
        json={"ids": ids},
        timeout=5,
    )
    if response.status_code != STATUS_DELETED:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
