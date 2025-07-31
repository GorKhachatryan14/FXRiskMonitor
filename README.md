# FXRiskMonitor 🇦🇲  
**LLM-Based Evaluation of Currency Exchange Transactions**

This project demonstrates how I fine-tuned a multilingual transformer-based language model to assess **currency exchange transactions** (e.g., AMD–USD, RUB–EUR) and automatically identify whether each transaction is **safe (ok)** or **potentially suspicious (red flag)**.

The model processes structured **multi-field JSON data** containing bilingual (Armenian-English) descriptions of each transaction. The pipeline includes **synthetic data generation**, **model fine-tuning**, and preparation for **API integration** in a production banking environment.

---

## 🧠 Project Background

As part of an internal initiative at the **Central Bank of Armenia**, I was assigned to develop an intelligent model for analyzing currency exchange transaction reports submitted by banks.

Due to the sensitive nature of real data, I created a robust **synthetic data generator** that mimics real financial FX transactions with realistic content in both **Armenian** and **English**.

Each synthetic JSON sample simulates a full transaction record and ends with a classification label:
- `"ok"` — safe/regular transaction
- `"red flag"` — potentially suspicious or non-compliant transaction

---

## 🔧 Pipeline Overview

### 1. 🔄 Synthetic Data Generation
- Designed field templates to simulate currency exchanges (amount, description, country, currency pair, etc.)
- Generated bilingual (EN+HY) textual content for each sample
- Assigned `"ok"` or `"red flag"` label based on rules and keyword logic

### 2. 🤖 Model Fine-Tuning
- Base model: `bert-base-multilingual-cased` (supports Armenian and English)
- Used Hugging Face `Trainer` API for efficient training
- Dataset split: 80% train / 20% test
- Achieved strong classification metrics (see below)

### 3. 🔌 API-Ready Model Export
- Saved trained model and tokenizer
- Wrote Python prediction wrapper: `predict(json_data) → label`
- Ready for integration into a banking system as part of FX compliance checks

---

## 💬 Example

**Input JSON:**
<details>
<summary>Click to expand</summary>

```json
{
  "Նույնականացուցիչ համար": "1572131072574",
  "Մասնաճյուղ": 15721,
  "Գործընկերոջ երկիր": "NCL",
  "Գործընկերոջ ռեզիդենտություն": "ռեզիդենտ",
  "Գործընկերոջ իրավական կարգավիճակ": "իրավաբանական անձ",
  "Գործընկերոջ հատվածային պատկանելիություն": "Բանկ",
  "Գործընկերոջ տնտեսության ճյուղ": "հրատարակչական գործ",
  "Առքի արժույթ": "UAH",
  "Վաճառքի արժույթ": "AMD",
  "Առքի ծավալ": 3964148,
  "Հրապարակային փոխարժեք": 10.04,
  "Փոխարժեք": 10.04,
  "Գումարի միջակայք": "20.000.000 – 40.000.000 դրամ",
  "Առքի իրականացման եղանակ": "անկանխիկ",
  "Վաճառքի իրականացման եղանակ": "կանխիկ",
  "Ում հաշվին է գործարքը կնքվել": "իր հաշվին",
  "Ում անունից է գործարքը կնքվել": "հաճախորդի անունից",
  "Գործարքի տեսակ": "անուղղակի",
  "Գործարքի ձև": "հաշվից կանխիկացում",
  "Գործարքի կատարման ամսաթիվ": "28/04/2024",
  "Ժամանակահատված": "12:07:44",
  "Գործարքների քանակ": 2,
  "Մեդիան": 3964148,
  "Ստանդարտ շեղում": 198208,
  "label": "red flag"
}
