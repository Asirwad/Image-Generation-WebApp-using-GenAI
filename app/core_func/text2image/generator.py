import json
import os
from diffusers import StableDiffusionXLPipeline
import requests
import streamlit
from PIL import Image
import io
import torch

API_URL_XL_BASE_1 = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
API_URL_V2 = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"


@streamlit.cache_resource(show_spinner=False)
def generate_image_cloud(prompt):
    with open("C:/Users/asirw/PycharmProjects/InvisiCipher/app/models/StableDiffusionAPI/Key.json") as file:
        key = json.load(file)[0]
    response = requests.post(API_URL_XL_BASE_1, headers={"Authorization": key}, json={"inputs": prompt})
    print(response)
    image = Image.open(io.BytesIO(response.content))
    return image


@streamlit.cache_resource(show_spinner=False)
def generate_image_locally(prompt, steps=10):
    # Check if the model exists locally
    model_path = "./Models/stable-diffusion-xl-base-1.0"
    if os.path.exists(model_path):
        # Load the model
        print("Model found")
        pipe = StableDiffusionXLPipeline.from_pretrained(model_path,
                                                         torch_dtype=torch.float16,
                                                         use_safetensors=True,
                                                         variant="fp16",
                                                         max_memory=100)
    else:
        pipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                                         torch_dtype=torch.float16,
                                                         use_safetensors=True,
                                                         variant="fp16",
                                                         max_memory=100)
        pipe.save_pretrained(model_path)

    pipe.enable_model_cpu_offload()

    # Generate image based on the prompt
    image = pipe(prompt=prompt,
                 num_inference_steps=steps,
                 num_images_per_prompt=1,
                 output_type='pil'
                 ).images[0]
    return image
