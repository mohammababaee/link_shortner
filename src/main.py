from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.link_shortner.router import router as link_router
from src.user.router import router as user_router

app = FastAPI()

app.include_router(link_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
