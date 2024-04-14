import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF
import requests
from PIL import Image
import io

from .DeepLabv3.utils import visualize_batched_gt

BASE_URL = "http://localhost:8000"


def get_generated_image(**kwargs):
    url = f"{BASE_URL}/mnist/generate_image"
    try:
        resp = requests.post(url, json=kwargs)
        if resp.status_code == 200:
            return Image.open(io.BytesIO(resp.content))
        else:
            print(f"Unexpected HTTP status code:\n{resp.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request failed:\n{e}")
        return None
    except IOError as e:
        print(f"Error processing image:\n{e}")
        return None


def postprocess_model_output(out, ori_h, ori_w):
    out = F.interpolate(out, size=max(ori_h, ori_w))
    out = TF.center_crop(out, output_size=(ori_w, ori_h))
    seg_map = torch.argmax(out, dim=1)
    return visualize_batched_gt(seg_map, n_cols=1)


def segment(img_path):
    url = f"{BASE_URL}/segmentation"
    resp = requests.post(url, files={"file": open(img_path, mode="rb")})
    out = torch.load(io.BytesIO(resp.content))[None, ...]
    image = Image.open(img_path).convert("RGB")
    ori_h, ori_w = image.size
    seg_image = postprocess_model_output(out=out, ori_h=ori_h, ori_w=ori_w)
    return seg_image


if __name__ == "__main__":
    img_path = "/Users/jongbeomkim/Desktop/workspace/ML-API/assignment3/resources/107177246-1673454132712-gettyimages-1246154739-AFP_336V8DZ.webp"
    seg_image = segment(img_path)
    seg_image.show()
