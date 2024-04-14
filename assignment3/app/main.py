import torch
from fastapi import FastAPI, Response, File, UploadFile
from fastapi.responses import StreamingResponse
from pathlib import Path
from PIL import Image
import cv2
import numpy as np
import io
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"DeepLabv3"))

from assignment3.DeepLabv3.utils import get_device, image_to_grid, modify_state_dict
from assignment3.DeepLabv3.model import ResNet101DeepLabv3
from schemas import UserInput
import albumentations as A
from albumentations.pytorch import ToTensorV2

app = FastAPI()

RES_DIR = Path(__file__).resolve().parent.parent/"resources"
MODEL_PARAMS = "/Users/jongbeomkim/Downloads/deeplabv3_voc2012.pth"
DEVICE = get_device()
state_dict = torch.load(str(MODEL_PARAMS), map_location=DEVICE)
MODEL = ResNet101DeepLabv3().eval()
MODEL.load_state_dict(modify_state_dict(state_dict["model"]))

IMG_SIZE = 513
MEAN = (0.457, 0.437, 0.404)
STD = (0.275, 0.271, 0.284)
transform = A.Compose(
    [
        A.LongestMaxSize(max_size=IMG_SIZE, interpolation=cv2.INTER_AREA),
        A.PadIfNeeded(
            min_height=IMG_SIZE,
            min_width=IMG_SIZE,
            border_mode=cv2.BORDER_CONSTANT,
            value=(0, 0, 0),
        ),
        # A.CenterCrop(height=img_size, width=img_size),
        A.Normalize(mean=MEAN, std=STD),
        ToTensorV2(),
    ],
)


def image_to_bytes(image):
    """
    Convert a PIL Image object to bytes in PNG format.
    This function takes a PIL Image object as input, saves it to an in-memory BytesIO buffer
    in PNG format, and returns the byte data representing the image.

    Args:
        `image` (`PIL.Image.Image`): A PIL Image object representing the image to be converted.

    Returns:
        bytes or `None`: The byte data of the converted image in PNG format, or `None` if an
            error occurs.

    Raises:
        Exception: If an error occurs during the image conversion process.
    """
    try:
        byte_stream = io.BytesIO()
        image.save(byte_stream, format="PNG")
        byte_stream.seek(0)
        return byte_stream.getvalue()
    except Exception as e:
        print(f"Error occurred while converting image to bytes:\n{e}")
        return None


@app.post("/segmentation")
async def segmentation(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    print(image.size)
    img = np.array(image)
    image = transform(image=img)["image"]
    with torch.inference_mode():
        out = MODEL(image[None, ...])
    output_bytes = io.BytesIO()
    torch.save(out[0], output_bytes)
    output_bytes.seek(0)
    return StreamingResponse(output_bytes, media_type="application/octet-stream")


@app.post("/mnist/generate_image")
async def generate_image(user_input: UserInput):
    """
    Generate an image using a conditional WGAN-GP model based on user input.

    Args:
        `user_input` (`UserInput`): User-defined input specifying the numbers and batch size
            for image generation.

    Returns:
        `Response`: A FastAPI Response object containing the generated image in PNG format.
    """
    latent_vec = torch.randn(
        size=(len(user_input.nums) * user_input.batch_size, MODEL.latent_dim), device=DEVICE,
    )
    label = torch.tensor(
        user_input.nums, dtype=torch.int32, device=DEVICE,
    ).repeat_interleave(user_input.batch_size)
    image = MODEL(latent_vec=latent_vec, label=label)
    image = image_to_grid(image, n_cols=user_input.batch_size, mean=0.5, std=0.5)
    img_bytes = image_to_bytes(image)
    return Response(content=img_bytes, media_type="image/png")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
