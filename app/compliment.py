import torch
import random
from typing import List

def generate_compliment(features: torch.Tensor) -> str:
    """
    Generate a polite compliment based on extracted image features.

    Args:
        features (torch.Tensor): Feature vector from image, expected shape [C] or [N, C].

    Returns:
        str: A generated compliment string.
    """
    # Compute feature "energy" for simple heuristic
    energy: float = float(features.norm().item())

    # Base compliment options
    base: List[str]
    if energy > 120:
        base = [
            "You look absolutely radiant today",
            "Your presence lights up the doorway",
            "You have an incredible energy about you"
        ]
    elif energy > 100:
        base = [
            "You're looking fantastic today",
            "You've got a great vibe going on",
            "You bring a warm presence with you"
        ]
    else:
        base = [
            "Hope you're having a wonderful day",
            "It's great to see you",
            "You have a kind and welcoming presence"
        ]

    # Playful endings
    endings: List[str] = [
        "— thanks for stopping by!",
        "— glad you're here!",
        "— wishing you a great rest of your day!",
        "— you made our doorbell's day!"
    ]

    compliment: str = f"{random.choice(base)} {random.choice(endings)}"
    return compliment
