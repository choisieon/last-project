import openai
from PIL import Image
import base64

def generate_avatar(image_file):
    with open(image_file, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    response = openai.images.generate_variation(
        image=img_base64,
        n=1,
        size="256x256"
    )
    
    avatar_url = response['data'][0]['url']
    return avatar_url