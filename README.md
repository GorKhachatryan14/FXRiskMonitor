# ⚖️ FXRiskMonitor: LLM-Based Evaluation of Currency Exchange Transactions

This project showcases how a multilingual transformer-based language model (LLM) can be fine-tuned to classify **currency exchange transactions** (e.g., AMD–USD, RUB–EUR) as either **normal ("ok")** or **potentially suspicious ("red flag")**, based on structured JSON input.

The model processes real-like, **bilingual synthetic data** (Armenian-English) that simulates the structure and terminology of official banking transaction reports.

---

## 🏛️ Context

Developed as part of an initiative at the **Central Bank of Armenia**, this tool aims to assist with **automated FX transaction monitoring** by identifying transactions that deviate from typical behavior — such as suspicious amounts, unusual countries, abnormal rates, or wash trading patterns.

Due to the confidential nature of real data, a **synthetic dataset generator** was built to replicate realistic transaction scenarios.

---

## 🔁 Pipeline Overview

### 1. 🧪 Synthetic Data Generation
- Generates structured JSON transactions with fields like: currency, amount, country, rate, execution time, and more
- Supports bilingual transaction descriptions: `"transaction_description_en"` and `"transaction_description_hy"`
- Injects realistic anomalies to label samples as `"red flag"` or `"ok"` using domain-driven rules (e.g., front-running, odd time, inflated amounts)

### 2. 🤖 Model Fine-Tuning
- Base model: `bert-base-multilingual-cased` (supports Armenian and English)
- Framework: [Hugging Face Transformers](https://huggingface.co/transformers/)
- Training method: `Trainer` API with 80/20 train/test split
- Evaluation metrics: Precision, Recall, F1-score

### 3. 🌐 Inference & API Deployment
- The model is exported along with tokenizer and a wrapper for real-time predictions:
```python
predict(json_data: dict) -> "ok" | "red flag"
```
- Designed for integration into **banking systems** and FX monitoring pipelines

---

## 📦 Example Transaction Input

```json
{
    "Նույնականացուցիչ համար": "1571901082545",
    "Մասնաճյուղ": 15719,
    "Գործընկերոջ երկիր": "WLF",
    "Գործընկերոջ ռեզիդենտություն": "ոչ ռեզիդենտ",
    "Գործընկերոջ իրավական կարգավիճակ": "իրավաբանական անձ",
    "Գործընկերոջ հատվածային պատկանելիություն": "Այլ ֆինանսական կազմակերպություն",
    "Գործընկերոջ տնտեսության ճյուղ": "հիմնային մետաղների արտադրություն",
    "Գործընկերոջ կոդ": "89055",
    "Գործընկերոջ՝ ֆինանսական կազմակերպության հետ կապվածություն": "կապված է",
    "Առքի արժույթ": "AMD",
    "Վաճառքի արժույթ": "CHF",
    "Առքի ծավալ": "",
    "Վաճառքի ծավալ": 423859,
    "Հրապարակային փոխարժեք": 445.0,
    "Փոխարժեք": 445.0,
    "Գումարի միջակայք": "400.000 – 1.500.000 դրամ",
    "Առքի իրականացման եղանակ": "անկանխիկ",
    "Վաճառքի իրականացման եղանակ": "անկանխիկ",
    "Ում հաշվին է գործարքը կնքվել": "իր հաշվին",
    "Ում անունից է գործարքը կնքվել": "իր անունից",
    "Գործարքի տեսակ": "ուղղակի",
    "Գործարքի ձև": "փոխանցում",
    "Գործարքի կատարման ամսաթիվ": "15/05/2024",
    "Գործարքի կնքման ամսաթիվ": "15/05/2024",
    "Ժամանակահատված": "08:38:08",
    "Գործարքի կնքման վայր": "ՀՀ չկարգավորվող շուկա",
    "Գործարքի իրականացման միջավայր": "վեբ համակարգ",
    "Առքի նվազագույն ծավալ": "",
    "Առքի առավելագույն ծավալ": "",
    "Վաճառքի նվազագույն ծավալ": 381473,
    "Վաճառքի առավելագույն ծավալ": 466245,
    "Մեդիան": 423859,
    "Ստանդարտ շեղում": 21193,
    "Գործարքների քանակ": 5,
}
```

**Classification Output:**
```json
"red flag"
```




