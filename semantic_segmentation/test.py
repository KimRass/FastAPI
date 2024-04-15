import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF
import requests
from PIL import Image
import io
import argparse

from .DeepLabv3.utils import visualize_batched_gt

BASE_URL = "http://3.141.143.48:8000"


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--img_path", type=str, required=True)
    parser.add_argument("--save_path", type=str, required=True)

    args = parser.parse_args()

    args_dict = vars(args)
    new_args_dict = dict()
    for k, v in args_dict.items():
        new_args_dict[k.upper()] = v
    args = argparse.Namespace(**new_args_dict)
    return args


def postprocess_model_output(out, ori_h, ori_w):
    out = F.interpolate(out, size=max(ori_h, ori_w))
    out = TF.center_crop(out, output_size=(ori_w, ori_h))
    seg_map = torch.argmax(out, dim=1)
    return visualize_batched_gt(seg_map, n_cols=1)


def segment(img_path):
    url = f"{BASE_URL}/segment"
    resp = requests.post(url, files={"file": open(img_path, mode="rb")})
    out = torch.load(io.BytesIO(resp.content))[None, ...]
    image = Image.open(img_path).convert("RGB")
    ori_h, ori_w = image.size
    seg_image = postprocess_model_output(out=out, ori_h=ori_h, ori_w=ori_w)
    return seg_image


if __name__ == "__main__":
    args = get_args()
    seg_image = segment(args.IMG_PATH)
    Image.blend(Image.open(args.IMG_PATH).convert("RGB"), seg_image, alpha=0.5).save(
        args.SAVE_PATH,
    )
