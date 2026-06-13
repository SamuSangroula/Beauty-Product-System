"""
Samu's WeCare Beauty Products System - Main Application
Entry point for the inventory management system.
"""
from datetime import datetime
from read import load_products, print_stock, display_menu, get_menu_choice
from write import save_products
from operation import handle_customer_purchase, handle_supplier_restock

def start_application():
    """Loads data and runs the main application loop."""
    # Load initial inventory using parallel lists
    item_names, item_brands, item_quantities, item_costs, item_origins = load_products()

    while True:
        display_menu()
        user_choice = get_menu_choice()

        if user_choice == '1':
            print_stock(item_names, item_brands, item_quantities, item_costs, item_origins)
        elif user_choice == '2':
            if not item_names:
                print("Inventory is empty. Cannot make a sale.")
                continue
            # Functions return the modified lists
            item_names, item_brands, item_quantities, item_costs, item_origins = \
                handle_customer_purchase(item_names, item_brands, item_quantities, item_costs, item_origins)
            # Save immediately after transaction
            save_products(item_names, item_brands, item_quantities, item_costs, item_origins)
        elif user_choice == '3':
            # Functions return the modified lists (potentially new items added)
            item_names, item_brands, item_quantities, item_costs, item_origins = \
                handle_supplier_restock(item_names, item_brands, item_quantities, item_costs, item_origins)
            # Save immediately after transaction
            save_products(item_names, item_brands, item_quantities, item_costs, item_origins)
        elif user_choice == '4':
            print("Saving inventory and exiting...")
            save_products(item_names, item_brands, item_quantities, item_costs, item_origins)
            print("Goodbye!")
            break

# Script entry point
if __name__ == "__main__":
    start_application()
