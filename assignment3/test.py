import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF
import requests
from PIL import Image
import numpy as np
import io

from assignment3.app.utils import visualize_batched_gt

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
    return torch.argmax(out, dim=1)


def segment(**kwargs):
    url = f"{BASE_URL}/segmentation"
    img_path = "/Users/jongbeomkim/Desktop/workspace/ML-API/assignment3/resources/107177246-1673454132712-gettyimages-1246154739-AFP_336V8DZ.webp"
    resp = requests.post(url, files={"file": open(img_path, mode="rb")})
    out = torch.load(io.BytesIO(resp.content))[None, ...]
    image = Image.open(img_path).convert("RGB")
    ori_h, ori_w = image.size
    seg_map = postprocess_model_output(out=out, ori_h=ori_h, ori_w=ori_w)
    seg_image = visualize_batched_gt(seg_map, n_cols=1)
    seg_image.save("/Users/jongbeomkim/Downloads/test.png")
    np.unique(np.array(seg_image))
    Image.blend(image, seg_image, alpha=0.5).show()

    Image.open(io.BytesIO(resp.content))
    print(type(resp.content))
    
    image = Image.open(io.BytesIO(resp.content))


if __name__ == "__main__":
    image = get_generated_image(batch_size=3, nums=[1, 1, 1, 9, 10])
    image.show()
