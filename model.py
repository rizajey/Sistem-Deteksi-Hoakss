import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ==========================================================
# LOKASI MODEL HASIL TRAINING
# ==========================================================

MODEL_PATH = "hoax detection model"

# ==========================================================
# LOAD TOKENIZER DAN MODEL
# ==========================================================

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.eval()

# ==========================================================
# FUNGSI PREDIKSI
# ==========================================================

def predict(text):

    # Tokenisasi
    inputs = tokenizer(
        text,
        max_length=128,
        truncation=True,
        padding="max_length",
        return_tensors="pt"
    )

    # Prediksi
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits

    # Probabilitas
    probabilities = torch.softmax(logits, dim=1)

    # Label prediksi
    prediction = torch.argmax(probabilities, dim=1).item()

    # Confidence
    confidence = probabilities[0][prediction].item()

    return prediction, confidence