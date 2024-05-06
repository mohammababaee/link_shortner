from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from link_shortner.router import router as link_router
from user.router import router as user_router

app = FastAPI()

app.include_router(link_router)
app.include_router(user_router)

