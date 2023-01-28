from dotenv import load_dotenv
import os 
import torch
from diffusers import StableDiffusionPipeline
from PIL.Image import Image

load_dotenv()
token = os.getenv('HF_TOKEN')

# get your token at https://huggingface.co/settings/tokens
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    revision="fp16",
    torch_dtype=torch.float16,
    use_auth_token=token,
)

pipe.to("mps")
# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

prompt = "a photograph of an astronaut riding a horse"

#Required as per huggin face documentation
_ = pipe(prompt, num_inference_steps=1)

#image = pipe(prompt).images[0]
#image = pipe(prompt)["sample"][0] Doest work


def obtain_image(
    prompt: str,
    *,
    seed: int | None = None,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
) -> Image:
    generator = None if seed is None else torch.Generator().manual_seed(seed)
    print(f"Using device: {pipe.device}")

    image: Image = pipe(
        prompt,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        generator=generator,
    ).images[0]
    return image


#image = obtain_image(prompt, num_inference_steps=5, seed=1024)