import torch
import random


def generate_compliment(features: torch.Tensor) -> str:
    """
    Generate a compliment based on extracted image features.
    This is intentionally simple and fun — easy to extend later.
    """

    # Basic heuristics based on feature magnitude
    energy = float(features.norm().item())

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

    # Add a playful ending
    endings = [
        "— thanks for stopping by!",
        "— glad you're here!",
        "— wishing you a great rest of your day!",
        "— you made our doorbell's day!"
    ]

    return f"{random.choice(base)} {random.choice(endings)}"

