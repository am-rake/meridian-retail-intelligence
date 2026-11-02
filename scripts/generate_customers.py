import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Read our existing store records
with open(data_folder / "stores.csv", newline="", encoding="utf-8") as file:
    stores = list(csv.DictReader(file))

# Fictional customer names
first_names = [
    "James", "Sarah", "Michael", "Emily", "David",
    "Jessica", "Daniel", "Ashley", "Robert", "Amanda",
    "Christopher", "Olivia", "Matthew", "Sophia",
    "Andrew", "Elizabeth", "Joshua", "Emma",
    "Ryan", "Hannah"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown",
    "Jones", "Garcia", "Miller", "Davis",
    "Wilson", "Anderson", "Thomas", "Taylor",
    "Moore", "Jackson", "Martin", "Lee",
    "Walker", "Hall", "Allen", "Young"
]

acquisition_channels = [
    "Organic Search",
    "Paid Advertising",
    "Social Media",
    "Referral",
    "Walk-In",
    "Email Campaign"
]

customers = []

# Generate 5,000 fictional customer records
for i in range(1, 5001):

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    customer_id = str(uuid.uuid5(
        uuid.NAMESPACE_DNS,
        f"meridian-customer-{i}"
    ))

    # Reserved example.com domain prevents real email delivery
    email = f"customer{i:05d}@example.com"

    preferred_store = random.choice(stores)

    acquisition_channel = random.choice(acquisition_channels)

    # Customer registration date
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 10, 31)

    days_between = (end_date - start_date).days

    created_at = start_date + timedelta(
        days=random.randint(0, days_between)
    )

    customers.append({
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "preferred_store_id": preferred_store["store_id"],
        "acquisition_channel": acquisition_channel,
        "created_at": created_at.strftime("%Y-%m-%d"),
        "hubspot_contact_id": ""
    })

output_file = data_folder / "customers.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "preferred_store_id",
            "acquisition_channel",
            "created_at",
            "hubspot_contact_id"
        ]
    )

    writer.writeheader()
    writer.writerows(customers)

print(f"Successfully generated {len(customers)} customers!")
print(f"File saved to: {output_file}")