import random
import string
import re


def link_validate(link: str):
    if not link.startswith(("http://", "https://")):
        link = f"http://{link}"
    return link


def generate_random_code(length=5):
    """
    Generate a random Base58 code of specified length.
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def is_valid_url(url):
    url_pattern = re.compile(
        r"^(https?://)?(www\.)?([a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+)([/\?]?[a-zA-Z0-9-_+%&=\.\(\)\\#]*)*/?$",
        re.IGNORECASE
    )
    return re.match(url_pattern, url) is not None
