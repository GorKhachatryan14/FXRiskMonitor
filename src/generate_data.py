
# FXRiskMonitor — Synthetic Transaction Generator (Refactored & Readable)

import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker(locale="hy_AM")

# --- Dataset Sizes ---
NUM_NORMAL = 4000
NUM_RED_FLAGS = 6000

# --- Sample Static Reference Data ---
REZIDENTUTYUN = ["ռեզիդենտ", "ոչ ռեզիդենտ"]
TESAK = ["ուղղակի", "անուղղակի"]
IRAVAKAN_KARGAVICHAK = ["ֆիզիկական անձ", "իրավաբանական անձ"]
PATKANELUTYUN = ["Բանկ", "Վարկային կազմակերպություն", "Ոչ ֆինանսական հատվածի կազմակերպություն"]
JYUX = ["անասնապահություն", "սննդի արդյունաբերություն", "ծխախոտի արդյունաբերություն"]
VCHARQI_TESAK = ["առք", "վաճառք"]
CURRENCIES = ["USD", "EUR", "RUB", "GBP"]
BASE_EXCHANGE_RATES = {
    "USD": 384.36, "EUR": 436.02, "RUB": 4.80, "GBP": 507.86
}

# --- Helpers ---
def get_amount_range(value):
    ranges = [
        (0, 100_000, "մինչև 100.000 դրամ"),
        (100_000, 400_000, "100.000 – 400.000 դրամ"),
        (400_000, 1_500_000, "400.000 – 1.500.000 դրամ"),
        (1_500_000, float("inf"), "1.500.000 դրամ և ավելի"),
    ]
    for low, high, label in ranges:
        if low <= value < high:
            return label
    return "Անհայտ միջակայք"

def random_date(start, end):
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%d/%m/%Y")

# --- Transaction Generator ---
def generate_transaction(label="ok"):
    date = random_date(datetime(2024, 1, 1), datetime(2024, 5, 20))
    currency = random.choice(CURRENCIES)
    exchange = round(BASE_EXCHANGE_RATES[currency] * random.choice([0.95, 1.0, 1.05]), 2)
    base_amount = random.randint(50_000, 5_000_000)
    vcharq_type = random.choice(VCHARQI_TESAK)
    arqi, vacharqi = (base_amount, round(base_amount * exchange)) if vcharq_type == "առք" else (round(base_amount / exchange), base_amount)

    return {
        "Նույնականացուցիչ համար": f"{random.randint(15700, 15730)}{datetime.now().strftime('%d%m%y')}{random.randint(1, 99):02d}",
        "Գործընկերոջ ռեզիդենտություն": random.choice(REZIDENTUTYUN),
        "Գործընկերոջ իրավական կարգավիճակ": random.choice(IRAVAKAN_KARGAVICHAK),
        "Գործընկերոջ հատվածային պատկանելիություն": random.choice(PATKANELUTYUN),
        "Գործընկերոջ տնտեսության ճյուղ": random.choice(JYUX),
        "Առքի արժույթ": currency if vcharq_type == "առք" else "AMD",
        "Վաճառքի արժույթ": currency if vcharq_type == "վաճառք" else "AMD",
        "Առքի ծավալ": arqi if vcharq_type == "առք" else "",
        "Վաճառքի ծավալ": vacharqi if vcharq_type == "վաճառք" else "",
        "Փոխարժեք": exchange,
        "Հրապարակային փոխարժեք": exchange,
        "Գումարի միջակայք": get_amount_range(max(arqi, vacharqi)),
        "Գործարքի կատարման ամսաթիվ": date,
        "Ժամանակահատված": f"{random.randint(8, 18):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}",
        "Գործարքների քանակ": random.randint(1, 5),
        "Label": label
    }

# --- Red Flag Transaction Generator ---
def generate_red_flag_transaction():
    tx = generate_transaction(label="red_flag")
    tx["Փոխարժեք"] *= random.choice([0.85, 1.15])  # manipulate rate
    tx["Գործարքների քանակ"] = random.randint(5, 10)  # simulate high-frequency
    tx["Ժամանակահատված"] = f"{random.randint(0, 3):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
    return tx

# --- Data Generation ---
data = [generate_transaction("ok") for _ in range(NUM_NORMAL)] + \
        [generate_red_flag_transaction() for _ in range(NUM_RED_FLAGS)]
random.shuffle(data)

with open("synthetic_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

