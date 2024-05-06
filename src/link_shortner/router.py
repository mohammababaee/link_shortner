from datetime import datetime
from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse

from link_shortner.models import Link

router = APIRouter()

@router.post("/shorten")  # Specify the endpoint path ("/shorten/")
async def create_short_link(link: str):
    pass
@router.get('/{shortned_link:path}')
async def redirect_to_path(shortned_link: str):
    pass
