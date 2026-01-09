from typing import Optional
from PIL import Image
import torch
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

# Device
_device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model once
_weights: EfficientNet_B0_Weights = EfficientNet_B0_Weights.DEFAULT
_model: torch.nn.Module = efficientnet_b0(weights=_weights)
_model.eval()
_model.to(_device)

# Use official transform
_transform: torch.nn.Module = _weights.transforms()

@torch.inference_mode()
def extract_features(image: Image.Image) -> torch.Tensor:
    tensor: torch.Tensor = _transform(image).unsqueeze(0).to(_device)
    features: torch.Tensor = _model.features(tensor)
    pooled: torch.Tensor = torch.nn.functional.adaptive_avg_pool2d(features, (1, 1))
    return pooled.squeeze().cpu()
