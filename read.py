"""
Read operations for Samu's WeCare Beauty Products System.
"""
from datetime import datetime


DATA_FILE = 'products.txt'


def load_products():
    """Reads inventory from the data file into separate lists."""
    names, brands, quantities, costs, origins = [], [], [], [], []
    try:
        with open(DATA_FILE, 'r') as file:
            lines = file.readlines()
        for line in lines:
            line = line
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 5:
                names.append(parts[0])
                brands.append(parts[1])
                try:
                    quantities.append(int(parts[2]))
                    costs.append(int(parts[3]))
                except ValueError:
                    print(f"Warning: Invalid number in line: {line}. Skipping.")

                    names.pop()
                    brands.pop()
                    continue
                origins.append(parts[4])
            else:
                pass
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found. Starting with empty inventory.")
    except IOError:
        print(f"Error reading {DATA_FILE}.")
    return names, brands, quantities, costs, origins

def get_selling_price(item_cost):
    """Calculates selling price based on markup."""
    MARKUP_PERCENTAGE = 200 
    return item_cost * (MARKUP_PERCENTAGE / 100.0)

def find_item_index(item_name, all_names):
    """Finds the index of an item, case-insensitive."""
    for i, name in enumerate(all_names):
        if name.lower() == item_name.lower():
            return i
    return -1 

def print_stock(names, brands, quantities, costs, origins):
    """Prints the current stock levels with selling prices."""
    print("\n--- Current Inventory ---")
    if not names:
        print("Inventory is empty.")
        return

    print(f"{'No.':<4} {'Item Name':<20} {'Brand':<15} {'Stock':>7} {'Sell Price':>12} {'Origin':<15}")
    print("-" * 80)
    for i in range(len(names)):
        sell_price = get_selling_price(costs[i])
        print(f"{i+1:<4} {names[i]:<20} {brands[i]:<15} {quantities[i]:>7} {sell_price:>12.2f} {origins[i]:<15}")
    print("-" * 80)


def display_menu():
    """Displays the main menu options."""
    print("\n=== WeCare Beauty Products System ===")
    print("1. View Current Stock")
    print("2. Process Customer Purchase")
    print("3. Process Supplier Restock")
    print("4. Exit System")

def get_menu_choice():
    """Gets a valid menu choice from the user."""
    valid_choices = ['1', '2', '3', '4']
    while True:
        choice = input("Enter your choice (1-4): ")
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please enter 1-4.")