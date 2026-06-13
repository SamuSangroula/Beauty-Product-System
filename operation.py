"""
Operation functions for Samu's WeCare Beauty Products System.
"""
from datetime import datetime
from read import print_stock, get_selling_price, find_item_index
from write import save_products, create_customer_invoice, create_supplier_invoice

def validate_name(name):
    if not name or name.isspace():
        return False, "Name cannot be empty."
    
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '-.,&"
    
    for char in name:
        if char not in allowed_chars:
            return False, f"Invalid character '{char}' in name. Use only letters, spaces, and basic punctuation."
    
    return True, ""

def get_valid_name(prompt):
    while True:
        name = input(prompt).strip()
        is_valid, error_message = validate_name(name)
        
        if is_valid:
            return name
        else:
            print(error_message)

# Handle customer purchase
def handle_customer_purchase(all_names, all_brands, all_quantities, all_costs, all_origins):
    """Manages the process of a customer buying items."""
    customer = get_valid_name("Enter customer name: ")
    purchase_list = []  # List of tuples: (index, qty_paid, qty_free, unit_sell_price)
    
    while True:
        print_stock(all_names, all_brands, all_quantities, all_costs, all_origins)
        choice = input("Enter item number to buy (or 'f' to finish): ").strip()
        if choice.lower() == 'f':
            break
            
        try:
            item_num = int(choice)
            if not (1 <= item_num <= len(all_names)):
                print("Invalid item number.")
                continue
            item_index = item_num - 1
        except ValueError:
            print("Invalid input. Please enter a number or 'f'.")
            continue
            
        item_name = all_names[item_index]
        available = all_quantities[item_index]
        
        while True:  # Quantity input loop
            try:
                qty_str = input(f"Enter quantity for {item_name} (Available: {available}): ")
                qty_to_buy = int(qty_str)
                if qty_to_buy <= 0:
                    print("Quantity must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid quantity.")
                
        # Calculate free items based on the "buy 3 get 1 free" policy
        qty_free = qty_to_buy // 3
        total_needed = qty_to_buy + qty_free
        
        if total_needed > available:
            print(f"Not enough stock. Need {total_needed} (incl. free), only {available} available.")
            continue
            
        # Add to purchase list (simple approach, overwrites if chosen again)
        found_in_list = False
        for i in range(len(purchase_list)):
            if purchase_list[i][0] == item_index:
                print(f"Updating quantity for {item_name}.")
                purchase_list[i] = (item_index, qty_to_buy, qty_free, get_selling_price(all_costs[item_index]))
                found_in_list = True
                break
        if not found_in_list:
            purchase_list.append((item_index, qty_to_buy, qty_free, get_selling_price(all_costs[item_index])))
            
        print(f"Added {qty_to_buy} (+{qty_free} free) {item_name} to cart.")
    
    if not purchase_list:
        print("No items purchased.")
        return all_names, all_brands, all_quantities, all_costs, all_origins  # Return unchanged
    
    # Create invoice and update inventory
    receipt_filename, grand_total = create_customer_invoice(customer, purchase_list, all_names, all_brands, all_quantities, all_costs, all_origins)
    
    # Update inventory quantities
    for index, qty_paid, qty_free, _ in purchase_list:
        total_taken = qty_paid + qty_free
        all_quantities[index] -= total_taken
    
    print(f"Sale complete. Total: INR {grand_total:.2f}")
    return all_names, all_brands, all_quantities, all_costs, all_origins

# Handle supplier restock
def handle_supplier_restock(all_names, all_brands, all_quantities, all_costs, all_origins):
    """Manages the process of restocking items from a supplier."""
    supplier = get_valid_name("Enter supplier name: ")
    restock_details = []  # List of tuples: (index | -1 for new, name, brand, origin, qty, cost)
    
    while True:
        item_name = get_valid_name("Enter item name to restock (or 'f' to finish): ")
        if item_name.lower() == 'f':
            break
            
        item_index = find_item_index(item_name, all_names)
        
        while True:  # Quantity loop
            try:
                qty_str = input(f"Enter quantity for {item_name}: ")
                qty_add = int(qty_str)
                if qty_add <= 0:
                    print("Quantity must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid quantity.")
                
        current_cost_str = f" (Current: {all_costs[item_index]})" if item_index != -1 else " (New Item)"
        while True:  # Cost loop
            try:
                cost_str = input(f"Enter cost price per item{current_cost_str}: ")
                item_cost = int(cost_str)
                if item_cost <= 0:
                    print("Cost must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid cost price.")
                
        brand, origin = "", ""
        if item_index == -1:  # New item
            brand = get_valid_name("Enter brand name: ")
            origin = get_valid_name("Enter country of origin: ")
            if not brand or not origin:
                print("Brand and origin cannot be empty for new items. Skipping.")
                continue        
            else:
                brand = all_brands[item_index]
                origin = all_origins[item_index]
            
        restock_details.append((item_index, item_name, brand, origin, qty_add, item_cost))
        print(f"Added {qty_add} of {item_name} to restock list.")
    
    if not restock_details:
        print("No items to restock.")
        return all_names, all_brands, all_quantities, all_costs, all_origins
    
    # Create invoice and update inventory
    invoice_filename, total_restock_cost = create_supplier_invoice(supplier, restock_details)
    
    # Update inventory with new quantities and costs
    new_names, new_brands, new_quantities, new_costs, new_origins = list(all_names), list(all_brands), list(all_quantities), list(all_costs), list(all_origins)
    
    for index, name, brand, origin, qty, cost in restock_details:
        if index != -1:  # Existing item
            new_quantities[index] += qty
            new_costs[index] = cost  # Update cost price
        else:  # New item
            new_names.append(name)
            new_brands.append(brand)
            new_quantities.append(qty)
            new_costs.append(cost)
            new_origins.append(origin)
    
    print(f"Restock complete. Total cost: INR {total_restock_cost}")
    return new_names, new_brands, new_quantities, new_costs, new_origins