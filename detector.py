
# detector.py
from ultralytics import YOLO

def load_model(model_path="model/best.pt"):
    model = YOLO(model_path)
    return model

def process_image(image, model):
    results = model(image)
    return results
