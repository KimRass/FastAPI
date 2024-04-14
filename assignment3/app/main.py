import torch
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from pathlib import Path
from PIL import Image
import numpy as np
import io
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"DeepLabv3"))

from ..DeepLabv3.utils import get_device, modify_state_dict
from ..DeepLabv3.model import ResNet101DeepLabv3
from ..DeepLabv3.voc2012 import VOC2012Dataset


app = FastAPI()

RES_DIR = Path(__file__).resolve().parent.parent/"resources"
DEVICE = get_device()
state_dict = torch.load(str(RES_DIR/"deeplabv3-voc2012.pt"), map_location=DEVICE)
MODEL = ResNet101DeepLabv3().eval()
MODEL.load_state_dict(modify_state_dict(state_dict))

TRANSFORM = VOC2012Dataset.get_val_transform(
    img_size=513,
    mean=(0.457, 0.437, 0.404),
    std=(0.275, 0.271, 0.284),
)


@app.post("/segmentation")
async def segmentation(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    img = np.array(image)
    image = TRANSFORM(image=img)["image"]
    with torch.inference_mode():
        out = MODEL(image[None, ...])
    output_bytes = io.BytesIO()
    torch.save(out[0], output_bytes)
    output_bytes.seek(0)
    return StreamingResponse(output_bytes, media_type="application/octet-stream")
