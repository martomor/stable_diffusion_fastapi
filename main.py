from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from ml import obtain_image

import io

app = FastAPI()


@app.get("/",response_class=HTMLResponse)
def home():
    return """
        <html>
            <head>
                <title>Stable Diffusion Fastapi</title>
            </head>
            <body>
                <h1>Welcome to the Stable Diffusion FastAPI implemention.</h1>
                <p>Please go to the docs section to consume the API</p>
            </body>
        </html>
        """


@app.get("/generate")
def generate_image(
        prompt: str,
        *,
        seed: int | None = None,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5):
    image = obtain_image(
        prompt=prompt, 
        num_inference_steps=num_inference_steps, 
        seed=seed,
        guidance_scale=guidance_scale)
    memory_stream = io.BytesIO() #To avoid writing into diskç
    image.save(memory_stream, format="PNG") #Fake fili in memory
    memory_stream.seek(0)
    return StreamingResponse(memory_stream, media_type="image/png")
