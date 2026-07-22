from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load the trained model once when the server starts
model = joblib.load('fraud_model.pkl')
THRESHOLD = 0.9

@app.get("/")
def home():
    return {"message": "Fraud Detection API is running"}

@app.post("/predict")
def predict(transaction: dict):
    # Convert the incoming transaction into a DataFrame (model expects this format)
    df = pd.DataFrame([transaction])
    
    # Get fraud probability
    proba = model.predict_proba(df)[0][1]
    is_fraud = bool(proba >= THRESHOLD)
    
    return {
        "fraud_probability": float(proba),
        "is_fraud": is_fraud
    }