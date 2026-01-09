from typing import Dict
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.vision import extract_features
from app.compliment import generate_compliment
from PIL import Image, UnidentifiedImageError
import io
import asyncio

app: FastAPI = FastAPI(title="Doorbell Compliment Service")

@app.post("/doorbell")
async def doorbell_endpoint(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Accepts an uploaded image, extracts features using a ML model, 
    and returns a polite compliment based on the image.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read image bytes asynchronously
    contents: bytes = await file.read()

    # Load image safely
    try:
        image: Image.Image = Image.open(io.BytesIO(contents)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Extract features (run in executor to avoid blocking the event loop)
    features = await asyncio.get_event_loop().run_in_executor(
        None, extract_features, image
    )

    # Generate compliment based on features
    compliment: str = generate_compliment(features)

    # Return strict type-annotated dictionary
    return {"compliment": compliment}


# Optional uvicorn entry point for direct run
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,  # Auto-reload in dev
        log_level="info"
    )