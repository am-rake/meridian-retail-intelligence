import csv
import random
from pathlib import Path

random.seed(42)

# Locate project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Read existing store records
with open(data_folder / "stores.csv", newline="", encoding="utf-8") as file:
    stores = list(csv.DictReader(file))

# Read existing product records
with open(data_folder / "products.csv", newline="", encoding="utf-8") as file:
    products = list(csv.DictReader(file))

inventory = []

# Create inventory for every store and product
for store in stores:
    for product in products:

        # Different categories carry different quantities
        category = product["category"]

        if category in ["Groceries", "Beverages"]:
            quantity = random.randint(0, 150)
            reorder_point = 30

        elif category in ["Electronics", "Home Automation"]:
            quantity = random.randint(0, 25)
            reorder_point = 5

        else:
            quantity = random.randint(0, 75)
            reorder_point = 15

        # Smaller stores generally carry less inventory
        if store["store_name"] in ["Morthal", "Falkreath"]:
            quantity = int(quantity * 0.5)

        # E-commerce warehouse carries more inventory
        if store["store_type"] == "E-commerce":
            quantity = int(quantity * 1.5)

        unit_cost = float(product["wholesale_cost_usd"])

        inventory_value = round(quantity * unit_cost, 2)

        if quantity == 0:
            status = "Out of Stock"
        elif quantity <= reorder_point:
            status = "Low Stock"
        else:
            status = "In Stock"

        inventory.append({
            "store_id": store["store_id"],
            "store_name": store["store_name"],
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "quantity_available": quantity,
            "unit_cost_usd": unit_cost,
            "inventory_value_usd": inventory_value,
            "reorder_point": reorder_point,
            "inventory_status": status
        })

# Save inventory records
output_file = data_folder / "inventory.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "store_id",
            "store_name",
            "product_id",
            "product_name",
            "quantity_available",
            "unit_cost_usd",
            "inventory_value_usd",
            "reorder_point",
            "inventory_status"
        ]
    )

    writer.writeheader()
    writer.writerows(inventory)

print(f"Successfully generated {len(inventory)} inventory records!")
print(f"File saved to: {output_file}")