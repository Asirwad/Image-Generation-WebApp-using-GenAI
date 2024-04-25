from diffusers import DiffusionPipeline
import torch
import os


def generate_image(prompt):
    # Check if the model exists locally
    model_path = "./Models/stable-diffusion-xl-base-1.0"
    if os.path.exists(model_path):
        # Load the model
        print("Model found")
        pipe = DiffusionPipeline.from_pretrained(model_path,
                                                 torch_dtype=torch.float16,
                                                 use_safetensors=True,
                                                 variant="fp16",
                                                 max_memory=100)
    else:
        pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                                 torch_dtype=torch.float16,
                                                 use_safetensors=True,
                                                 variant="fp16",
                                                 max_memory=100)
        pipe.save_pretrained(model_path)

    pipe.enable_model_cpu_offload()

    # Generate image based on the prompt
    image = pipe(prompt=prompt, num_inference_steps=20).images[0]
    image.show()
    image.save('image.png')


# Example usage:
prompt = "a kerala girl in white saree"
generate_image(prompt)