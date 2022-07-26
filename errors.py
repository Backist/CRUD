"""Some General errors for improve database error handling."""

from enum import Enum


class Errors(Enum):
    """User ``__repr__`` method to print the name of the enum. (See more details in the documentation)\n
    ## NOTE: This is a general error class.

    - member: The error message.
    - name: Display member name
    - __repr__: Print the name of the enum.

    ### Attributes:
        DatabaseCredentialsError (int): Error code for invalid username or password.
        DatabaseConnectionError (int): Error code for invalid database connection.
        DatabaseError (int): Error code for general database error.
    
    """
    INITIALIZATION_ERROR = 1
    CONNECTION_ERROR = 2
    CREDENTIALS_ERROR = 3
    DATABASE_ERROR = 4
    DATABASE_DELETE_ERROR = 5
    DATABASE_INSERT_ERROR = 6
    DATABASE_UPDATE_ERROR = 7
    DATABASE_SELECT_ERROR = 8

    
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

