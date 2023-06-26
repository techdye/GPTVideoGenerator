from PIL import Image
import requests
from io import BytesIO


def get_image_online(url: str):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

