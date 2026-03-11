import numpy as np
import pandas as pd
from app.models.model_loader import model


def predict_from_csv(filepath):

    df = pd.read_csv(filepath)

    data = df.values / 255.0
    data = data.reshape(-1, 28, 28, 1)

    preds = model.predict(data)

    labels = np.argmax(preds, axis=1)

    return labels