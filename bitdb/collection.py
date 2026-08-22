from .document import generate_id
from .exceptions import (
    DuplicateDocumentError,
    InvalidDocumentError,
)


class Collection:
    def __init__(
        self,
        name: str,
        database,
        unique_fields: list[str] | None = None
    ):
        self.name = name
        self.database = database
        self.unique_fields = unique_fields or []

    def get_data(self) -> list[dict]:
        return self.database.data[self.name]

    def insert_one(self, document: dict) -> str:
        if not isinstance(document, dict):
            raise InvalidDocumentError(
                "Document must be a dictionary."
            )

        for existing in self.get_data():
            for field in self.unique_fields:
                if existing.get(field) == document.get(field):
                    raise DuplicateDocumentError(
                        f"Document with {field}="
                        f"{document.get(field)!r} already exists."
                    )

        existing_ids = {
            item["_id"]
            for item in self.get_data()
            if "_id" in item
        }

        document = document.copy()

        document["_id"] = generate_id(existing_ids)

        self.get_data().append(document)
        self.database._save()

        return document["_id"]

    def insert_many(self, documents: list[dict]) -> list[str]:
        ids = []

        for document in documents:
            ids.append(self.insert_one(document))

        return ids

    def find(self, **filters) -> list[dict]:
        result = []

        for document in self.get_data():
            for key, value in filters.items():
                if document.get(key) == value:
                    result.append(document)
                    break

        return result

    def find_one(self, **filters) -> dict | None:
        for document in self.get_data():
            for key, value in filters.items():
                if document.get(key) == value:
                    return document

        return None

    def update_one(
        self,
        key: str,
        value,
        updates: dict
    ) -> bool:
        for document in self.get_data():
            if document.get(key) == value:
                document.update(updates)
                self.database._save()
                return True

        return False

    def delete_one(self, key: str, value) -> bool:
        for document in self.get_data():
            if document.get(key) == value:
                self.get_data().remove(document)
                self.database._save()
                return True

        return False

    def count(self) -> int:
        return len(self.get_data())

    def clear(self) -> None:
        self.get_data().clear()
        self.database._save()