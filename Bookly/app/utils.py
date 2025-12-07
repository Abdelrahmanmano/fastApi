from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # First hash with SHA-256 to ensure it's always 64 bytes
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha256_hash)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)

class Hashing:
    @staticmethod
    def bcrypt(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str):
        return pwd_context.verify(plain_password, hashed_password)