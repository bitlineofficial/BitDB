from uuid import uuid4


def generate_id(existing_ids: set[str]) -> str:
    while True:
        document_id = f"jx_{uuid4().hex[:12]}"

        if document_id not in existing_ids:
            return document_id