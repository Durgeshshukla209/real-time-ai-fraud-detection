import pandas as pd
import requests
import time
import json

# Load the same test data your model was evaluated on
df = pd.read_csv('data/creditcard.csv')
X = df.drop('Class', axis=1)
y = df['Class']

# Use the last 1000 rows to simulate a live stream (keeps it quick to run)
stream_data = df.tail(1000)

API_URL = "http://127.0.0.1:8000/predict"

print("Starting live transaction stream... (Ctrl+C to stop)\n")

for idx, row in stream_data.iterrows():
    transaction = row.drop('Class').to_dict()
    actual_label = row['Class']
    
    response = requests.post(API_URL, json=transaction)
    result = response.json()
    
    flag = "🚨 FRAUD FLAGGED" if result['is_fraud'] else "✅ normal"
    actual = "(was actually fraud)" if actual_label == 1 else ""
    
    print(f"Txn {idx}: {flag} | probability={result['fraud_probability']:.4f} {actual}")
    
    time.sleep(0.3)  # simulate transactions arriving every 300ms