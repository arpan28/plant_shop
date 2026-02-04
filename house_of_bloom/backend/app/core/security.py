from passlib.context import CryptContext

# Use a bcrypt-free default to avoid the bcrypt backend issues seen in the container.
# pbkdf2_sha256 accepts arbitrarily long passwords and does not depend on the bcrypt package.
# Note: existing users whose passwords are stored with bcrypt/bcrypt_sha256 will not be
# automatically verified if the bcrypt backend is broken in your environment. Plan a
# migration (re-hash on next successful login or run a migration job) if needed.
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    deprecated="auto",
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a stored hash.
    Returns False on any verification error.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as exc:
        # verification failed (could be unknown scheme or backend error)
        # don't raise here — return False so caller treats it as invalid credentials.
        # Log if you want to inspect issues in the server logs.
        # Example: logger.warning("password verify error", exc_info=exc)
        return False

def get_password_hash(password: str) -> str:
    """
    Hash a password for storage using the configured default (pbkdf2_sha256).
    pbkdf2_sha256 supports long passwords and avoids the bcrypt 72-byte limit.
    """
    return pwd_context.hash(password)
