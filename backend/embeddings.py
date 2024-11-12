import sys
sys.path.append("C:\\Users\\Saba Gul\Desktop\\Celeb-Twin")
from facenet_pytorch import InceptionResnetV1
import torch
from PIL import Image
import io
from torchvision import transforms
import numpy as np

# Load FaceNet model
model = InceptionResnetV1(pretrained='vggface2').eval()

# Define image preprocessing pipeline
preprocess = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

def generate_embedding(image_bytes: bytes):
    # Convert bytes to an image
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    # Preprocess image
    img_tensor = preprocess(img).unsqueeze(0)  # Add batch dimension

    # Generate embedding
    with torch.no_grad():
        embedding = model(img_tensor)
    
    return embedding.squeeze().numpy()  # Convert to numpy array
