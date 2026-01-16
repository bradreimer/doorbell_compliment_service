"""
FastAPI application entry point.
"""

from __future__ import annotations

import io
import urllib.request

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image

from app.compliment import generate_compliment
from app.vision import extract_features

app = FastAPI(title="Doorbell Compliment Service")


class DoorbellRequest(BaseModel):
    """Request body for doorbell endpoint."""

    image_url: str


@app.post("/doorbell")
async def doorbell_endpoint(request: DoorbellRequest) -> dict[str, str]:
    """
    Accept an image URL and return a generated compliment.

    Args:
        request: Request containing the image URL.

    Returns:
        JSON containing a compliment.
    """
    try:
        with urllib.request.urlopen(request.image_url, timeout=10) as response:
            contents = response.read()
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail=f"Failed to download image: {str(exc)}"
        ) from exc

    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except OSError as exc:
        raise HTTPException(
            status_code=400, detail="Invalid image file"
        ) from exc

    features = extract_features(image)
    compliment = generate_compliment(features)

    return {"compliment": compliment}
