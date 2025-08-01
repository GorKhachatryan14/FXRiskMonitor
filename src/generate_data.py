
# FXRiskMonitor — Synthetic Transaction Generator
# ----------------------------------------------
# Generates labeled synthetic currency exchange transactions in Armenian and English
# for fine-tuning LLMs to detect suspicious financial activity

import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker(locale="hy_AM")

NUM_NORMAL = 4000
NUM_RED_FLAGS = 6000

REZIDENTUTYUN = ["ռեզիդենտ", "ոչ ռեզիդենտ"]
TESAK = ["ուղղակի", "անուղղակի"]
IRAVAKAN_KARGAVICHAK = ["ֆիզիկական անձ", "իրավաբանական անձ", "անհատ ձեռնարկատեր"]
VCHARQI_TESAK = ["առք", "վաճառք"]
KAPVACUTYUN = ["կապված է", "կապված չէ"]
FORM = ["հաշվի համալրում", "հաշվից կանխիկացում", "փոխանցում", "վճարում"]
MIJAVAYR = ["առերես", "վեբ համակարգ", "բջջային հավելված", "ՊՈՍ (POS) տերմինալ", "ՖԳԻԱՍ", "վիրտուալ ՊՈՍ (POS)"]
YEGHANAQ = ["կանխիկ", "անկանխիկ"]
HASHVI_TESAK = ["իր հաշվին", "հաճախորդի հաշվին"]
ANUN_TESAK = ["իր անունից", "հաճախորդի անունից"]
VAYR = ["ոչ ՀՀ չկարգավորվող շուկա", "ՀՀ չկարգավորվող շուկա"]

CURRENCIES = [
    "USD", "EUR", "RUB", "GBP", "CNY", "CHF", "AUD", "CAD",
    "JPY", "PLN", "AED", "SEK", "NOK", "CZK", "KZT", "TRY", "UAH", "GEL"
]

BASE_EXCHANGE_RATES = {
    "USD": 384.36, "EUR": 436.02, "RUB": 4.8037, "GBP": 507.86,
    "CNY": 54.45, "CHF": 445.00, "CAD": 274.80, "AUD": 249.57,
    "JPY": 2.669, "PLN": 101.91, "AED": 107.44, "SEK": 39.06,
    "NOK": 36.26, "CZK": 17.01, "KZT": 0.793, "TRY": 36.05,
    "UAH": 9.56, "GEL": 141.83
}

def get_amount_range(value_amd: float) -> str:
    ranges = [
        (0, 100_000, "մինչև 100.000 դրամ"),
        (100_000, 400_000, "100.000 – 400.000 դրամ"),
        (400_000, 1_500_000, "400.000 – 1.500.000 դրամ"),
        (1_500_000, 3_000_000, "1.500.000 – 3.000.000 դրամ"),
        (3_000_000, 6_000_000, "3.000.000 – 6.000.000 դրամ"),
        (6_000_000, 11_000_000, "6.000.000 – 11.000.000 դրամ"),
        (11_000_000, 20_000_000, "11.000.000 – 20.000.000 դրամ"),
        (20_000_000, 40_000_000, "20.000.000 – 40.000.000 դրամ"),
        (40_000_000, 80_000_000, "40.000.000 – 80.000.000 դրամ"),
        (80_000_000, 220_000_000, "80.000.000 – 220.000.000 դրամ"),
        (220_000_000, 800_000_000, "220.000.000 – 800.000.000 դրամ"),
        (800_000_000, float("inf"), "800.000.000 դրամ և ավելի"),
    ]
    for lower, upper, label in ranges:
        if lower <= value_amd < upper:
            return label
    return "Անհայտ միջակայք"

def random_date(start: datetime, end: datetime) -> str:
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%d/%m/%Y")

def generate_transaction(label="ok") -> dict:
    transaction_count = random.randint(1, 5)
    seq_num = f"{random.randint(1, 99):02d}"
    date_str = datetime.now().strftime('%d%m%y')
    org_code = str(random.randint(15700, 15730))
    ident_number = f"{org_code}{date_str}{seq_num}"
    currency = random.choice(CURRENCIES)
    multiplier = random.choice([0.95, 1.0, 1.05])
    exchange = round(BASE_EXCHANGE_RATES[currency] * multiplier, 2)
    base_amount = random.randint(50_000, 5_000_000)
    vcharq_type = random.choice(VCHARQI_TESAK)
    date = random_date(datetime(2024, 1, 1), datetime(2024, 5, 20))
    hour, minute, second = random.randint(8, 18), random.randint(0, 59), random.randint(0, 59)

    if transaction_count == 1:
        min_volume = max_volume = median = base_amount
        std_dev = 0
    else:
        min_volume = round(base_amount * 0.9)
        max_volume = round(base_amount * 1.1)
        median = round((min_volume + max_volume) / 2)
        std_dev = round((max_volume - min_volume) / 4)

    if vcharq_type == "առք":
        arqi = base_amount
        vacharqi = round(arqi * exchange)
        arqi_nvazaguyn, arqi_aravelaguyn = min_volume, max_volume
        vacharqi_nvazaguyn = vacharqi_aravelaguyn = ""
        amount_range = vacharqi
    else:
        vacharqi = base_amount
        arqi = round(vacharqi / exchange)
        vacharqi_nvazaguyn, vacharqi_aravelaguyn = min_volume, max_volume
        arqi_nvazaguyn = arqi_aravelaguyn = ""
        amount_range = vacharqi

    return {
        "Նույնականացուցիչ համար": ident_number,
        "Մասնաճյուղ": int(org_code),
        "Առքի արժույթ": currency if vcharq_type == "առք" else "AMD",
        "Վաճառքի արժույթ": currency if vcharq_type == "վաճառք" else "AMD",
        "Առքի ծավալ": arqi if vcharq_type == "առք" else "",
        "Վաճառքի ծավալ": vacharqi if vcharq_type == "վաճառք" else "",
        "Հրապարակային փոխարժեք": exchange,
        "Փոխարժեք": exchange,
        "Գումարի միջակայք": get_amount_range(amount_range),
        "Գործարքի կատարման ամսաթիվ": date,
        "Ժամանակահատված": f"{hour:02d}:{minute:02d}:{second:02d}",
        "Առքի նվազագույն ծավալ": arqi_nvazaguyn,
        "Առքի առավելագույն ծավալ": arqi_aravelaguyn,
        "Վաճառքի նվազագույն ծավալ": vacharqi_nvazaguyn,
        "Վաճառքի առավելագույն ծավալ": vacharqi_aravelaguyn,
        "Մեդիան": median,
        "Ստանդարտ շեղում": std_dev,
        "Գործարքների քանակ": transaction_count,
        "Label": label
    }

if __name__ == "__main__":
    data = [generate_transaction("ok") for _ in range(NUM_NORMAL)] +            [generate_transaction("red_flag") for _ in range(NUM_RED_FLAGS)]
    random.shuffle(data)

    os.makedirs("data", exist_ok=True)
    with open("data/synthetic_sample.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
