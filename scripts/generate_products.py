import csv
import random
from pathlib import Path

# Make generated results reproducible
random.seed(42)

# Locate the project's data folder
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"
data_folder.mkdir(exist_ok=True)

output_file = data_folder / "products.csv"

# Fallout-inspired product catalog
catalog = {
	"Nuka-Cola": {
		"category": "Beverages",
		"products": [
			"Nuka-Cola",
			"Nuka-Cola Quantum",
			"Nuka-Cherry",
			"Nuka-Cola Orange",
			"Nuka-Cola Grape"
		],
		"price_range": (2.99, 12.99)
	},
	"RobCo Industries": {
		"category": "Electronics",
		"products": [
			"Pip-Boy 3000",
			"RobCo Terminal",
			"Protectron",
			"RobCo Sensor Module"
		],
		"price_range": (149.99, 2499.99)
	},
	"General Atomics": {
		"category": "Home Automation",
		"products": [
			"Mister Handy",
			"Mister Gutsy",
			"Household Automation Unit"
		],
		"price_range": (499.99, 3999.99)
	},
	"BlamCo": {
		"category": "Groceries",
		"products": [
			"BlamCo Mac & Cheese",
			"BlamCo Family Pack"
		],
		"price_range": (2.49, 14.99)
	},
	"Sugar Bombs": {
		"category": "Groceries",
		"products": [
			"Sugar Bombs Cereal",
			"Sugar Bombs Family Size"
		],
		"price_range": (3.99, 11.99)
	},
	"Abraxo": {
		"category": "Household",
		"products": [
			"Abraxo Cleaner",
			"Abraxo Industrial Cleaner"
		],
		"price_range": (4.99, 29.99)
	},
	"Vault-Tec": {
		"category": "Apparel",
		"products": [
			"Vault 111 Jumpsuit",
			"Vault-Tec Utility Backpack",
			"Vault-Tec Survival Kit"
		],
		"price_range": (24.99, 199.99)
	},
	"Hubris Comics": {
		"category": "Entertainment",
		"products": [
			"Grognak the Barbarian",
			"Unstoppables Comic",
			"Silver Shroud Collectible"
		],
		"price_range": (9.99, 79.99)
	}
}

# Fictional retail variations
variations = [
	"Standard",
	"Deluxe",
	"Collector's Edition",
	"Limited Edition",
	"Value Pack",
	"Premium",
	"Classic",
	"Anniversary Edition",
	"Retail Exclusive",
	"Online Exclusive"
]

products = []
product_names = set()
product_id = 1

# Generate 250 unique product records
while len(products) < 250:

	brand = random.choice(list(catalog.keys()))
	details = catalog[brand]

	base_product = random.choice(details["products"])
	variation = random.choice(variations)

	product_name = f"{base_product} - {variation} - Series {product_id:03d}"
	# Prevent duplicate product names
	if product_name in product_names:
		continue

	minimum, maximum = details["price_range"]

	retail_price = round(random.uniform(minimum, maximum), 2)

	# Wholesale cost is 45%-75% of retail price
	wholesale_cost = round(
		retail_price * random.uniform(0.45, 0.75), 2
	)

	gross_profit = round(retail_price - wholesale_cost, 2)

	gross_margin = round(
		(gross_profit / retail_price) * 100, 2
	)

	products.append({
		"product_id": f"PRD-{product_id:03d}",
		"product_name": product_name,
		"brand": brand,
		"category": details["category"],
		"retail_price_usd": retail_price,
		"wholesale_cost_usd": wholesale_cost,
		"gross_profit_usd": gross_profit,
		"gross_margin_pct": gross_margin
	})
	product_names.add(product_name)

	product_id += 1

# Save products to CSV
with open(output_file, "w", newline="", encoding="utf-8") as file:

	writer = csv.DictWriter(
		file,
		fieldnames=[
			"product_id",
			"product_name",
			"brand",
			"category",
			"retail_price_usd",
			"wholesale_cost_usd",
			"gross_profit_usd",
			"gross_margin_pct"
		]
	)

	writer.writeheader()
	writer.writerows(products)

print(f"Successfully generated {len(products)} products!")
print(f"File saved to: {output_file}")
