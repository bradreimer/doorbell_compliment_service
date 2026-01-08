import torch
from torchvision import models, transforms
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

# Pretrained ImageNet model (baseline)
model = models.resnet18(weights="IMAGENET1K_V1")
model.eval().to(device)

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
])

# Minimal label set (placeholder)
LABELS = ["something interesting", "a person", "an object", "a visitor"]

def describe_image(image_path: str) -> str:
    img = Image.open(image_path).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)

    # Placeholder logic
    return "I see a visitor who looks absolutely wonderful today."

