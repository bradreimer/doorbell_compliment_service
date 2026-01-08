import torch
import torchvision.transforms as T
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

# Load model once at startup
_weights = EfficientNet_B0_Weights.DEFAULT
_model = efficientnet_b0(weights=_weights)
_model.eval()

# Preprocessing pipeline
_transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=_weights.meta["mean"], std=_weights.meta["std"])
])


@torch.inference_mode()
def extract_features(image):
    """
    Takes a PIL image and returns a feature vector (tensor).
    """
    tensor = _transform(image).unsqueeze(0)
    features = _model.features(tensor)
    pooled = torch.nn.functional.adaptive_avg_pool2d(features, (1, 1))
    return pooled.squeeze().cpu()

