
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv
from database import users_collection
from user.models import User
from user.utils import authenticate_user, create_access_token, generate_salt, get_password_hash, verify_password
import uuid


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@router.post("/register")
async def register_user(email: str, password: str):
    user_exist = users_collection.find_one({"email": email})
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    salt = generate_salt()
    hashed_password = get_password_hash(password,salt)
    user_id = str(uuid.uuid4())
    while users_collection.find_one({"id": user_id}):
        user_id = str(uuid.uuid4())
    user = User(email=email, hashed_password=hashed_password,salt=salt, id=user_id,created_date=datetime.now())
    users_collection.insert_one(user.dict(by_alias=True))
    return {"message": "User registered successfully", "user_details": user.dict()}


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    load_dotenv()
    exp_minuets = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    access_token_expires = timedelta(minutes=exp_minuets)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}   