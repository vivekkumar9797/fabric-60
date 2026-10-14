"""
Generates a synthetic BFSI lending dataset for the fabric-60 project.

Outputs (in ./sample-data/):
  customers.csv          ~20,000 customers
  loan_applications.csv  ~50,000 applications

Deliberate data-quality issues are injected so the Week 2 bronze->silver
notebooks have real cleaning work to do:
  - ~0.5% duplicate application_id rows
  - ~2% null annual_income, ~1% null cibil_score
  - inconsistent city casing / stray whitespace
  - a few negative loan_amount values
  - mixed date formats in ~1% of application_date values

Run:  python generate_loan_data.py
"""

import csv
import os
import random
from datetime import date, timedelta

random.seed(42)

OUT_DIR = "sample-data"
N_CUSTOMERS = 20_000
N_APPLICATIONS = 50_000

CITIES = [
    ("Bengaluru", "Karnataka"), ("Mumbai", "Maharashtra"), ("Pune", "Maharashtra"),
    ("Delhi", "Delhi"), ("Gurugram", "Haryana"), ("Hyderabad", "Telangana"),
    ("Chennai", "Tamil Nadu"), ("Kolkata", "West Bengal"), ("Ahmedabad", "Gujarat"),
    ("Jaipur", "Rajasthan"), ("Lucknow", "Uttar Pradesh"), ("Kochi", "Kerala"),
]
EMPLOYMENT = ["Salaried", "Self-Employed", "Business", "Retired"]
PRODUCTS = {
    # product: (min_amt, max_amt, min_tenure, max_tenure, base_rate)
    "Personal Loan": (50_000, 2_500_000, 12, 60, 11.5),
    "Home Loan": (1_000_000, 15_000_000, 120, 360, 8.6),
    "Auto Loan": (300_000, 2_000_000, 12, 84, 9.2),
    "Gold Loan": (20_000, 1_500_000, 3, 36, 9.9),
    "Credit Card": (25_000, 500_000, 1, 1, 36.0),
    "Business Loan": (200_000, 7_500_000, 12, 84, 13.0),
}
CHANNELS = ["Branch", "Mobile App", "NetBanking", "DSA", "Partner"]


def rand_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))


def messy_city(city: str) -> str:
    r = random.random()
    if r < 0.03:
        return city.upper()
    if r < 0.06:
        return city.lower()
    if r < 0.08:
        return f" {city} "
    return city


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---------- customers ----------
    customers = []
    for i in range(1, N_CUSTOMERS + 1):
        city, state = random.choice(CITIES)
        emp = random.choices(EMPLOYMENT, weights=[60, 20, 15, 5])[0]
        base_income = {"Salaried": 900_000, "Self-Employed": 1_100_000,
                       "Business": 1_600_000, "Retired": 500_000}[emp]
        income = int(random.lognormvariate(0, 0.55) * base_income)
        customers.append({
            "customer_id": f"C{i:06d}",
            "date_of_birth": rand_date(date(1960, 1, 1), date(2004, 12, 31)).isoformat(),
            "city": messy_city(city),
            "state": state,
            "employment_type": emp,
            "annual_income": "" if random.random() < 0.02 else income,
            "cibil_score": "" if random.random() < 0.01 else random.randint(300, 900),
            "customer_since": rand_date(date(2010, 1, 1), date(2026, 6, 30)).isoformat(),
        })

    with open(os.path.join(OUT_DIR, "customers.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(customers[0].keys()))
        w.writeheader()
        w.writerows(customers)

    # ---------- loan applications ----------
    rows = []
    for i in range(1, N_APPLICATIONS + 1):
        cust = random.choice(customers)
        product = random.choices(list(PRODUCTS), weights=[30, 12, 15, 10, 25, 8])[0]
        mn, mx, tmin, tmax, base_rate = PRODUCTS[product]
        amount = round(random.uniform(mn, mx), -3)
        if random.random() < 0.002:
            amount = -amount  # bad data
        tenure = random.randint(tmin, tmax)

        cibil = cust["cibil_score"] if cust["cibil_score"] != "" else random.randint(300, 900)
        risk_adj = max(0.0, (750 - int(cibil)) / 100)
        rate = round(base_rate + risk_adj + random.uniform(-0.5, 0.75), 2)

        app_date = rand_date(date(2023, 1, 1), date(2026, 9, 30))
        app_date_str = app_date.isoformat()
        if random.random() < 0.01:
            app_date_str = app_date.strftime("%d/%m/%Y")  # mixed format

        # approval / default logic loosely tied to credit score
        approve_p = min(0.95, max(0.05, (int(cibil) - 450) / 400))
        r = random.random()
        if r < approve_p:
            status = "Approved"
        elif r < approve_p + 0.05:
            status = "Pending"
        else:
            status = "Rejected"

        defaulted = ""
        if status == "Approved":
            default_p = max(0.01, (720 - int(cibil)) / 900) + (0.03 if product == "Personal Loan" else 0)
            defaulted = 1 if random.random() < default_p else 0

        rows.append({
            "application_id": f"APP{i:07d}",
            "customer_id": cust["customer_id"],
            "application_date": app_date_str,
            "product": product,
            "channel": random.choice(CHANNELS),
            "loan_amount": amount,
            "tenure_months": tenure,
            "interest_rate": rate,
            "existing_emi_monthly": random.choice([0, 0, 0, round(random.uniform(2_000, 80_000), -2)]),
            "status": status,
            "defaulted": defaulted,
        })

    # inject ~0.5% duplicates
    dupes = random.sample(rows, k=int(N_APPLICATIONS * 0.005))
    rows.extend(dict(d) for d in dupes)
    random.shuffle(rows)

    with open(os.path.join(OUT_DIR, "loan_applications.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"customers.csv:         {len(customers):,} rows")
    print(f"loan_applications.csv: {len(rows):,} rows (incl. {len(dupes)} duplicates)")


if __name__ == "__main__":
    main()
