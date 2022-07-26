"""Some General errors for improve database error handling."""

__all__ = [
    "DatabaseInitializationError",
    "DatabaseConnectionError",
    "DatabaseQueryError",
    "DatabaseUpdateError",
    "DatabaseDeleteError",
    "DatabaseInsertError",
    "DatabaseSelectError",
    "DatabaseError",
    "DatabaseCredentialsError",
]

class DatabaseInitializationError(Exception):
    """
    Clases para manejar los errores u excepciones de la clase Database.
    """
    ...

class DatabaseConnectionError(Exception):
    """
    Clases para manejar los errores u excepciones de la clase Database.
    """
    ...

class DatabaseQueryError(Exception):
    ...

class DatabaseUpdateError(Exception):
    ...

class DatabaseDeleteError(Exception):
    ...

class DatabaseInsertError(Exception):
    ...

class DatabaseSelectError(Exception):
    ...

class DatabaseError(Exception):
    ...

class DatabaseCredentialsError(Exception):
    ...