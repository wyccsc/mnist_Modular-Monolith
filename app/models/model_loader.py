from tensorflow.keras.models import load_model
from app.config import MODEL_PATH

model = load_model(MODEL_PATH)