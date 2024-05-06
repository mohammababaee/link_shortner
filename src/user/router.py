
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from pydantic import BaseModel
from dotenv import load_dotenv
from os import getenv
from database import users_collection
from user.models import User
from user.utils import authenticate_user, create_access_token, get_password_hash


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# User registration endpoint
@router.post("/register")
async def register_user(email: str, password: str):
    user_exist = users_collection.find_one({"email": email})
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password)
    users_collection.insert_one(user.dict(by_alias=True))
    return {"message": "User registered successfully", "user_details": user.dict()}


# Token generation endpoint
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    load_dotenv()
    exp_minuets = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    access_token_expires = timedelta(minutes=exp_minuets)
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}   
