import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Real-Time Fraud Detection", layout="wide")
st.title("🔍 Real-Time Fraud Detection Dashboard")

API_URL = "http://127.0.0.1:8000/predict"

# Load data to simulate the stream
df = pd.read_csv('data/creditcard.csv')
# Mix normal transactions with guaranteed fraud cases for a better demo
normal_sample = df[df['Class'] == 0].sample(180, random_state=42)
fraud_sample = df[df['Class'] == 1].sample(20, random_state=42)
stream_data = pd.concat([normal_sample, fraud_sample]).sample(frac=1, random_state=1)  # shuffle them together

# Placeholders that we'll keep updating
col1, col2, col3 = st.columns(3)
total_placeholder = col1.empty()
fraud_placeholder = col2.empty()
rate_placeholder = col3.empty()

table_placeholder = st.empty()

if st.button("Start Live Stream"):
    flagged_transactions = []
    total_count = 0
    fraud_count = 0

    for idx, row in stream_data.iterrows():
        transaction = row.drop('Class').to_dict()
        actual_label = row['Class']

        response = requests.post(API_URL, json=transaction)
        result = response.json()

        total_count += 1
        if result['is_fraud']:
            fraud_count += 1
            flagged_transactions.append({
                "Transaction ID": idx,
                "Amount": transaction['Amount'],
                "Fraud Probability": f"{result['fraud_probability']:.2%}",
                "Actually Fraud": "Yes" if actual_label == 1 else "No"
            })

        # Update the live metrics
        total_placeholder.metric("Transactions Processed", total_count)
        fraud_placeholder.metric("Fraud Flagged", fraud_count)
        rate_placeholder.metric("Flag Rate", f"{(fraud_count/total_count)*100:.2f}%")

        # Update the table of flagged transactions
        if flagged_transactions:
            table_placeholder.dataframe(pd.DataFrame(flagged_transactions), use_container_width=True)

        time.sleep(0.1)

    st.success("Stream complete!")