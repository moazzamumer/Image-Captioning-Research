from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load the BLIP model and processor
model_name = "trained_blip_model"
processor = BlipProcessor.from_pretrained(model_name)
model = BlipForConditionalGeneration.from_pretrained(model_name)

# Load the image
image_path = "limelight.jpg"  # Replace with your image path
image = Image.open(image_path).convert("RGB")  # Ensure the image is in RGB format

# Preprocess the image for the model
inputs = processor(images=image, return_tensors="pt")

# Generate the caption
model.eval()  # Ensure the model is in evaluation mode
with torch.no_grad():
    outputs = model.generate(**inputs)

# Decode the generated caption
caption = processor.decode(outputs[0], skip_special_tokens=True)
print("Generated Caption:", caption)
