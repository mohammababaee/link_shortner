import random
import string


def link_validate(link: str):
    if not link.startswith(("http://", "https://")):
        link = f"http://{link}"
    return link


def generate_random_code(length=6):
    """
    Generate a random Base58 code of specified length.
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))
