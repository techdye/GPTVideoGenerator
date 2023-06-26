from PIL import Image
import requests
from io import BytesIO


def get_image_online(url: str) -> Image:
    response = requests.get(url)
    return Image.open(BytesIO(response.content))
