import os
import pandas as pd
from app.config import UPLOAD_FOLDER, RESULT_FILE


def save_uploaded_file(file_bytes, filename):

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file_bytes)

    return filepath


def save_predictions(labels):

    df = pd.DataFrame({"Label": labels})

    df.to_csv(RESULT_FILE, index=False)

    return RESULT_FILE