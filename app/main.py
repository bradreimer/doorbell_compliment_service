"""
FastAPI application entry point.
"""

from __future__ import annotations

import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image

from app.compliment import generate_compliment
from app.vision import extract_features

app = FastAPI(title="Doorbell Compliment Service")


@app.post("/doorbell")
async def doorbell_endpoint(file: UploadFile = File(...)) -> dict[str, str]:
    """
    Accept an image and return a generated compliment.

    Args:
        file: Uploaded image file.

    Returns:
        JSON containing a compliment.
    """
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()

    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except OSError as exc:
        raise HTTPException(
            status_code=400, detail="Invalid image file"
        ) from exc

    features = extract_features(image)
    compliment = generate_compliment(features)

    return {"compliment": compliment}
