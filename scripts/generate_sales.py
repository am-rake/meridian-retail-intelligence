import csv
import random
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

random.seed(42)

# Locate project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Read existing datasets
def read_csv(filename):
    with open(
        data_folder / filename,
        newline="",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


stores = read_csv("stores.csv")
products = read_csv("products.csv")
customers = read_csv("customers.csv")

# Make sure our existing datasets loaded
assert len(stores) == 9, "Expected 9 locations"
assert len(products) == 250, "Expected 250 products"
assert len(customers) == 5000, "Expected 5000 customers"

# Store sales volume weights
# Higher weights mean more transactions
store_weights = {
    "Whiterun": 20,
    "Solitude": 14,
    "Windhelm": 10,
    "Riften": 12,
    "Markarth": 13,
    "Falkreath": 6,
    "Dawnstar": 7,
    "Morthal": 4,
    "Tamriel Online": 18
}

# Product category purchase frequency
category_weights = {
    "Beverages": 30,
    "Groceries": 25,
    "Household": 15,
    "Apparel": 10,
    "Entertainment": 10,
    "Electronics": 7,
    "Home Automation": 3
}

# Customer purchase frequency
# Some customers purchase more frequently
customer_weights = [
    random.choices(
        [1, 2, 3, 5],
        weights=[40, 35, 20, 5]
    )[0]
    for _ in customers
]

# Use Decimal for financial calculations
def money(value):
    return Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


orders = []
order_items = []

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 10, 31)

total_days = (end_date - start_date).days

# Prepare product selection weights
product_weights = [
    category_weights.get(
        product["category"], 5
    )
    for product in products
]

# Generate 25,000 orders
for order_number in range(1, 25001):

    store = random.choices(
        stores,
        weights=[
            store_weights.get(
                s["store_name"], 5
            )
            for s in stores
        ]
    )[0]

    customer = random.choices(
        customers,
        weights=customer_weights
    )[0]

    # Generate a random order date
    order_date = start_date + timedelta(
        days=random.randint(0, total_days),
        hours=random.randint(9, 20),
        minutes=random.randint(0, 59)
    )

    # Select 1-4 different products
    item_count = random.choices(
        [1, 2, 3, 4],
        weights=[45, 35, 15, 5]
    )[0]

    selected_products = random.choices(
        products,
        weights=product_weights,
        k=item_count
    )

    # Remove duplicate products
    selected_products = list({
        p["product_id"]: p
        for p in selected_products
    }.values())

    order_id = f"ORD-{order_number:06d}"

    order_revenue = Decimal("0.00")
    order_cost = Decimal("0.00")

    for item_number, product in enumerate(
        selected_products, start=1
    ):

        quantity = random.choices(
            [1, 2, 3],
            weights=[80, 15, 5]
        )[0]

        unit_price = money(
            product["retail_price_usd"]
        )

        unit_cost = money(
            product["wholesale_cost_usd"]
        )

        # Discounts between 0% and 15%
        discount_pct = random.choices(
            [0, 5, 10, 15],
            weights=[70, 15, 10, 5]
        )[0]

        discount_multiplier = (
            Decimal("100") - Decimal(discount_pct)
        ) / Decimal("100")

        discounted_price = money(
            unit_price * discount_multiplier
        )

        line_revenue = money(
            discounted_price * quantity
        )

        line_cost = money(
            unit_cost * quantity
        )

        line_profit = money(
            line_revenue - line_cost
        )

        order_revenue += line_revenue
        order_cost += line_cost

        order_items.append({
            "order_item_id": (
                f"{order_id}-{item_number:02d}"
            ),
            "order_id": order_id,
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price_usd": unit_price,
            "discount_pct": discount_pct,
            "net_revenue_usd": line_revenue,
            "cost_of_goods_usd": line_cost,
            "gross_profit_usd": line_profit
        })

    order_profit = money(
        order_revenue - order_cost
    )

    orders.append({
        "order_id": order_id,
        "customer_id": customer["customer_id"],
        "store_id": store["store_id"],
        "order_date": order_date.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "sales_channel": (
            "E-commerce"
            if store["store_type"] == "E-commerce"
            else "Retail"
        ),
        "order_status": "Completed",
        "order_total_usd": money(order_revenue),
        "cost_of_goods_usd": money(order_cost),
        "gross_profit_usd": order_profit
    })

# Save CSV files
def save_csv(filename, records, columns):

    output_file = data_folder / filename

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=columns
        )

        writer.writeheader()
        writer.writerows(records)

    print(f"Created {filename}: {len(records)} records")


save_csv(
    "orders.csv",
    orders,
    [
        "order_id",
        "customer_id",
        "store_id",
        "order_date",
        "sales_channel",
        "order_status",
        "order_total_usd",
        "cost_of_goods_usd",
        "gross_profit_usd"
    ]
)

save_csv(
    "order_items.csv",
    order_items,
    [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price_usd",
        "discount_pct",
        "net_revenue_usd",
        "cost_of_goods_usd",
        "gross_profit_usd"
    ]
)

print()
print("Sales data generation complete!")
print(f"Total orders: {len(orders):,}")
print(f"Total order items: {len(order_items):,}")

total_revenue = sum(
    Decimal(str(order["order_total_usd"]))
    for order in orders
)

total_profit = sum(
    Decimal(str(order["gross_profit_usd"]))
    for order in orders
)

print(f"Total revenue: ${total_revenue:,.2f}")
print(f"Total gross profit: ${total_profit:,.2f}")