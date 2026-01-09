"""
Compliment generation based on visual features.
"""

from __future__ import annotations

from typing import Dict, Union
import random

FeatureMap = Dict[str, Union[float, bool]]

ENERGY_HIGH_THRESHOLD: float = 120.0
ENERGY_MEDIUM_THRESHOLD: float = 100.0
BRIGHTNESS_THRESHOLD: float = 140.0
COLORFULNESS_THRESHOLD: float = 70.0


def generate_compliment(features: FeatureMap) -> str:
    """
    Generate a positive, appearance-focused compliment.

    Args:
        features: Visual cues extracted from an image.

    Returns:
        A friendly compliment string.
    """
    phrases: list[str] = []

    if bool(features.get("has_face")):
        phrases.append(
            random.choice(
                (
                    "Your expression feels warm and welcoming",
                    "You have a very friendly presence",
                    "That look carries quiet confidence",
                )
            )
        )

    if float(features.get("brightness", 0.0)) > BRIGHTNESS_THRESHOLD:
        phrases.append(
            random.choice(
                (
                    "The lighting really suits you",
                    "You stand out beautifully in this light",
                )
            )
        )

    if float(features.get("colorfulness", 0.0)) > COLORFULNESS_THRESHOLD:
        phrases.append(
            random.choice(
                (
                    "Your outfit has great color and personality",
                    "Those colors work wonderfully together",
                )
            )
        )

    if bool(features.get("centered")):
        phrases.append(
            random.choice(
                (
                    "You carry yourself with calm confidence",
                    "You look comfortable and at ease",
                )
            )
        )

    if not phrases:
        phrases.append(
            random.choice(
                (
                    "You have a kind and welcoming presence",
                    "You bring a really nice energy with you",
                )
            )
        )

    ending = random.choice(
        (
            "Thanks for stopping by!",
            "Hope the rest of your day is great!",
            "Great to see you today!",
            "You just made the doorbell smile!",
        )
    )

    return f"{random.choice(phrases)} {ending}"
