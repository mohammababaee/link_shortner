from passlib.context import CryptContext
from database import users_collection
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
from os import getenv
import secrets
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password,salt, hashed_password):
    return pwd_context.verify(plain_password + salt, hashed_password)

def get_password_hash(password,salt):
    return pwd_context.hash(password+ salt)


async def authenticate_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user:
        return False
    if not verify_password(password, user["salt"],user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    load_dotenv()
    SECRET_KEY = getenv("SECRET_KEY")
    ALGORITHM = getenv("ALGORITHM")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_salt(length: int = 16) -> str:
    """Generate a random salt."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))