from passlib.context import CryptContext
from typing import Final

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# NOTE: In a complete application, 'bcrypt' would be configured via a 
#       settings module (e.g., from app.core.config import settings), 
#       allowing easy changes to hashing schemes and deprecation policies.

# Define the global CryptContext instance.
# Schemes=["bcrypt"] is the currently recommended scheme for robust password hashing.
# 'deprecated="auto"' automatically handles upgrading old hashes when a user logs in.
pwd_context: Final[CryptContext] = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
)

# ----------------------------------------------------------------------
# Public Functions
# ----------------------------------------------------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored hash.

    This function uses the configured CryptContext (bcrypt) to safely compare
    the input password with the hash retrieved from the database. It prevents
    timing attacks inherent in simple string comparisons.

    Args:
        plain_password: The password provided by the user (e.g., login input).
        hashed_password: The securely stored hash retrieved from the database.

    Returns:
        True if the passwords match, False otherwise.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # Handles cases where the hashed_password format is invalid or null
        return False

def get_password_hash(password: str) -> str:
    """
    Generates a secure, salted hash for a given plain-text password.

    The returned hash string includes the algorithm identifier, salt, and hash 
    value, as determined by the CryptContext configuration (bcrypt).

    Args:
        password: The plain-text password to be hashed.

    Returns:
        The securely salted and hashed password string.
    """
    return pwd_context.hash(password)
