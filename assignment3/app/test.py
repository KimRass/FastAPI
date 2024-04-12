import requests
from PIL import Image
import io

BASE_URL = "http://localhost:8000"


# def upload_image(filename):
#     url = f"{BASE_URL}/upload/image/"
#     files = {"image": open(filename, "rb")}
#     resp = requests.post(url, files=files)
#     return resp


# def send_image_to_server(image_filename):
#     url = "http://localhost:8000/receive/image/"
#     data = {"image": open(image_filename, "rb")}
#     resp = requests.post(url, data=data)
#     return resp


def get_generated_image(batch_size):
    url = f"{BASE_URL}/mnist/generate_image/"
    data = {"batch_size": batch_size}
    print(data)
    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        return Image.open(io.BytesIO(resp.content))
image = get_generated_image(batch_size=3)
image.show()


if __name__ == "__main__":
