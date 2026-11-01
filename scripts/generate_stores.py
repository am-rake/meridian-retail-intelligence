import csv
from pathlib import Path

# Locate the project's data folder
project_folder = Path(__file__).resolve().parent.parent
output_file = project_folder / "data" / "stores.csv"

# Define our fictional retail locations
stores = [
	["STR-001", "Whiterun", "Retail", "Central", "Flagship"],
	["STR-002", "Solitude", "Retail", "Northwest", "Premium"],
	["STR-003", "Windhelm", "Retail", "Northeast", "Established"],
	["STR-004", "Riften", "Retail", "Southeast", "High Traffic"],
	["STR-005", "Markarth", "Retail", "West", "High Revenue"],
	["STR-006", "Falkreath", "Retail", "South", "Small Market"],
	["STR-007", "Dawnstar", "Retail", "North", "Seasonal"],
	["STR-008", "Morthal", "Retail", "Northwest", "Developing"],
	["WEB-001", "Tamriel Online", "E-commerce", "Online", "Digital"],
]

# Create the CSV file
with output_file.open("w", newline="", encoding="utf-8") as file:
	writer = csv.writer(file)
	writer.writerow([
		"store_id",
		"store_name",
		"store_type",
		"region",
		"store_profile",
	])
	writer.writerows(stores)

print(f"Successfully created {len(stores)} locations!")
print(f"File saved to: {output_file}")