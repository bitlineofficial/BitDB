class JexDBError(Exception):
    """Base exception for JexDB."""


class DuplicateDocumentError(JexDBError):
    """Raised when a duplicate document is inserted."""


class InvalidDocumentError(JexDBError):
    """Raised when a document has an invalid format."""


class CollectionNotFoundError(JexDBError):
    """Raised when a collection does not exist."""


class DocumentNotFoundError(JexDBError):
    """Raised when a document does not exist."""