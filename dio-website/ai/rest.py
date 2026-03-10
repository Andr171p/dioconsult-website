import requests
from dio_website_cms.settings.dev import FASTAPI_RAG

from .constants import STATUS_CREATED


def upload_document(file: bytes) -> list:
    response = requests.post(  # noqa: S113
        url=f"{FASTAPI_RAG}/api/v1/documents/upload",
        files={"file": file},
    )
    if response.status_code != STATUS_CREATED:
        raise Exception(f"API returned status {response.status_code}: {response.text}")  # noqa: TRY002
    return response.json()
