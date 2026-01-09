"""
Vision utilities for extracting visual cues from images.
"""

from __future__ import annotations

from typing import Dict, Union

import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision.models import EfficientNet_B0_Weights, efficientnet_b0

# ---- Constants -------------------------------------------------------------

IMAGE_SIZE: tuple[int, int] = (224, 224)
CENTER_CROP_RATIO: float = 0.5
FACE_SCALE_FACTOR: float = 1.3
FACE_MIN_NEIGHBORS: int = 5

# ---- Model Initialization --------------------------------------------------

WEIGHTS: EfficientNet_B0_Weights = EfficientNet_B0_Weights.DEFAULT
MODEL = efficientnet_b0(weights=WEIGHTS)
MODEL.eval()

TRANSFORM = transforms.Compose(
    [
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=WEIGHTS.transforms().mean,
            std=WEIGHTS.transforms().std,
        ),
    ]
)

FACE_CASCADE = cv2.CascadeClassifier(
    f"{cv2.data.haarcascades}haarcascade_frontalface_default.xml"
)

# ---- Public API ------------------------------------------------------------


@torch.inference_mode()
def extract_features(image: Image.Image) -> Dict[str, Union[float, bool]]:
    """
    Extract interpretable visual features from an image.

    Args:
        image: Input image in RGB format.

    Returns:
        Dictionary of visual cues.
    """
    tensor = TRANSFORM(image).unsqueeze(0)
    features = MODEL.features(tensor)
    pooled = torch.nn.functional.adaptive_avg_pool2d(features, (1, 1))
    energy = float(torch.norm(pooled).item())

    image_np = np.asarray(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    brightness = float(gray.mean())
    colorfulness = float(image_np.std())

    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=FACE_SCALE_FACTOR,
        minNeighbors=FACE_MIN_NEIGHBORS,
    )

    has_face = bool(len(faces))

    height, width = gray.shape
    crop_h = int(height * CENTER_CROP_RATIO)
    crop_w = int(width * CENTER_CROP_RATIO)

    y_start = (height - crop_h) // 2
    x_start = (width - crop_w) // 2

    center_crop = gray[y_start : y_start + crop_h, x_start : x_start + crop_w]
    centered = float(center_crop.mean()) >= brightness * 0.95

    return {
        "energy": energy,
        "brightness": brightness,
        "colorfulness": colorfulness,
        "has_face": has_face,
        "centered": centered,
    }
