# Real-Time AI Fraud Detection System

A real-time fraud detection system built with a machine learning model (XGBoost) served via a live API, with a streaming simulation and visual dashboard.

## 🔗 Live Demo
**[Try it live here](https://real-time-ai-fraud-detection-mhpt8bjtnaur8gypgt8fsk.streamlit.app/)** — click "Start Live Stream" to watch transactions being scored in real-time.

*Note: The backend API runs on a free-tier server and may take 30-50 seconds to "wake up" if it's been idle.*

## Overview

This project detects fraudulent credit card transactions in real-time by combining a trained ML model with a lightweight streaming architecture — transactions are scored the moment they arrive, not in batch.

## Architecture

Transaction stream → FastAPI (ML scoring) → Dashboard (live results)

## Results

- **ROC-AUC**: 0.97
- **Precision**: 0.81 (at tuned threshold of 0.9)
- **Recall**: 0.83
- Class imbalance handled via `scale_pos_weight` (fraud is only 0.173% of transactions)

## Tech Stack

Python, XGBoost, scikit-learn, FastAPI, Streamlit, pandas

## Dataset

[Credit Card Fraud Detection Dataset (Kaggle, by ULB)](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

## Future Improvements

- Replace simulated streaming with Apache Kafka for true production-grade event streaming
- Add a graph-based model to detect coordinated fraud rings
- Deploy the API and dashboard to the cloud

## How to Run

Install dependencies:  

```bash
pip install -r requirements.txt
uvicorn app:app --reload          # start the API
streamlit run dashboard.py        # start the dashboard (in a new terminal)
```