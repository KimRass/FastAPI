import torch
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response
import io
from PIL import Image
from fastapi.encoders import jsonable_encoder

from utils import image_to_grid
from model import Generator

app = FastAPI()

MODEL_PARAMS = "/home/jbkim/Desktop/workspace/ML-API/assignment3/resources/cwgan_gp_mnist.pth"
DEVICE = torch.device("cuda")
state_dict = torch.load(str(MODEL_PARAMS), map_location=DEVICE)
# model = ConditionalWGANGP()
model = Generator(n_classes=10, latent_dim=100, hidden_dim=32).to(DEVICE)
model.load_state_dict(state_dict)


# @app.post("/upload/image/")
# async def upload_image(image: UploadFile = File(...)):
#     # 이미지 파일을 받아서 처리
#     contents = await image.read()
#     # 여기에서 이미지를 처리하고 원하는 작업을 수행
#     return JSONResponse(
#         content={"message": "Image uploaded successfully"}, status_code=200,
#     )


# @app.post("/receive/image/")
# async def receive_image(image: UploadFile = File(...)):
#     # 클라이언트로부터 업로드된 이미지를 받아서 처리
#     contents = await image.read()
#     # 여기에서 이미지를 저장하거나 원하는 작업을 수행
#     with open(f"received_{image.filename}", "wb") as f:
#         f.write(contents)
#     return JSONResponse(
#         content={"message": "Image received and saved"}, status_code=200,
#     )


@app.post("/mnist/generate_image/")
async def generate_image(batch_size: int = 1):
    print(batch_size)
    latent_vec = torch.randn(
        size=(model.n_classes * batch_size, model.latent_dim), device=DEVICE,
    )
    label = torch.arange(
        model.n_classes, dtype=torch.int32, device=DEVICE,
    ).repeat_interleave(batch_size)
    # print(latent_vec.shape, label.shape)
    image = model(latent_vec=latent_vec, label=label)
    image = image_to_grid(image, n_cols=batch_size, mean=0.5, std=0.5)

    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)
    return Response(content=img_byte_array.getvalue(), media_type="image/png")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
