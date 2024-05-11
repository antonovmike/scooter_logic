from passlib.context import CryptContext

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """
    Hashes a password.

    Parameters:
    - password (str): The password to hash.

    Returns:
    - str: The hashed password.
    """
    return pwd_context.hash(password)
# hashed_password: Column[str]
def verify(plain_password: str, hashed_password: str):
    """
    Verifies a password against a hashed password.

    Parameters:
    - plain_password (str): The password to verify.
    - hashed_password (str): The hashed password to compare against.

    Returns:
    - bool: True if the password is valid, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
