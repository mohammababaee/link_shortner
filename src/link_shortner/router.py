from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from starlette.responses import RedirectResponse
from link_shortner.models import Link
from link_shortner.utils import generate_random_code, link_validate
from database import link_collection

router = APIRouter()


@router.post("/shorten")
async def create_short_link(link: str):
    """
    Endpoint to shorten a given link.
    """
    try:
        url = link_validate(link)
        # Generate a random Base58 code
        shortened_link_code = generate_random_code()

        # Check if the generated code exists in the database
        while link_collection.find_one({"shortned_link": shortened_link_code}):
            shortened_link_code = generate_random_code()
        shortened_link = Link(
            link=url,
            shortned_link=shortened_link_code,
            created_date=datetime.now(),
        )
        link_collection.insert_one(shortened_link.model_dump(by_alias=True))
        shortened_link = f"localhost:8000/{shortened_link_code}"
        return {
            "message": "Link shortened successfully",
            "shortened_link": shortened_link,
        }
    except ValueError as ve:
        raise HTTPException(
            status_code=400, detail=str(ve)
        )  # Bad Request for invalid URL
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{shortened_link:path}")
async def redirect_to_path(shortened_link: str):
    """
    Endpoint to redirect to the original link from the shortened one.
    """
    try:
        link_exist = link_collection.find_one(
            {"shortned_link": shortened_link}, max_time_ms=5000
        )
        if link_exist:
            print(link_exist)
            return RedirectResponse(url=link_exist["link"])
        else:
            raise HTTPException(status_code=404, detail="Link Not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
