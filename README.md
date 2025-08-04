#  FXRiskMonitor: LLM-Based Evaluation of Currency Exchange Transactions

This project showcases how a multilingual transformer-based language model (LLM) can be fine-tuned to classify **currency exchange transactions** (e.g., AMD–USD, RUB–EUR) as either **normal ("ok")** or **potentially suspicious ("red flag")**, based on structured JSON input.

The model processes real-like, **bilingual synthetic data** (Armenian-English) that simulates the structure and terminology of official banking transaction reports.

---

##  Context

Developed as part of an initiative at the **Central Bank of Armenia**, this tool aims to assist with **automated FX transaction monitoring** by identifying transactions that deviate from typical behavior — such as suspicious amounts, unusual countries, abnormal rates, or wash trading patterns.

Due to the confidential nature of real data, a **synthetic dataset generator** was built to replicate realistic transaction scenarios.

---

##  Pipeline Overview

### 1.  Synthetic Data Generation
- Generates structured JSON transactions with fields like: currency, amount, country, rate, execution time, and more
- Supports bilingual transaction descriptions: `"transaction_description_en"` and `"transaction_description_hy"`
- Injects realistic anomalies to label samples as `"red flag"` or `"ok"` using domain-driven rules (e.g., front-running, odd time, inflated amounts)

### 2.  Model Fine-Tuning
- Base model: `bert-base-multilingual-cased` (supports Armenian and English)
- Framework: [Hugging Face Transformers](https://huggingface.co/transformers/)
- Training method: `Trainer` API with 80/20 train/test split
- Evaluation metrics: Precision, Recall, F1-score

### 3.  Inference & API Deployment
- The model is exported along with tokenizer and a wrapper for real-time predictions:
```python
predict(json_data: dict) -> "ok" | "red flag"
```
- Designed for integration into **banking systems** and FX monitoring pipelines

---





