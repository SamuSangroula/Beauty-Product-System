"""
Write operations for Samu's WeCare Beauty Products System.
"""
from datetime import datetime


DATA_FILE = 'products.txt'

def save_products(names, brands, quantities, costs, origins):
    """Writes the current inventory state back to the data file."""
    try:
        with open(DATA_FILE, 'w') as file:
            for i in range(len(names)):
                line = f"{names[i]},{brands[i]},{quantities[i]},{costs[i]},{origins[i]}\n"
                file.write(line)
    except IOError:
        print(f"Error: Could not write inventory to {DATA_FILE}.")


def create_receipt_filename(type_indicator):
    """Generates a unique receipt filename using timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{type_indicator}_{timestamp}.txt"


def record_receipt(filename, data):
    """Writes receipt data to a file."""
    try:
        with open(filename, 'w') as file:
            file.write(data)
        print(f"Receipt saved: {filename}")
    except IOError as e:
        print(f"Error: Could not save receipt {filename}. {str(e)}")


def create_customer_invoice(customer, purchase_list, names, brands, quantities, costs, origins):
    """Creates and saves a customer sales invoice."""
    receipt_lines = []
    receipt_lines.append("=== WeCare Customer Receipt ===")
    receipt_lines.append(f"Customer: {customer}")
    receipt_lines.append(f"Date: {datetime.now()}")
    receipt_lines.append("\nItems:")
    receipt_lines.append(f"{'Item':<20} {'Brand':<15} {'Paid':>5} {'Free':>5} {'Total':>5} {'Price':>10} {'Cost':>10}")
    receipt_lines.append("-" * 75)
    
    grand_total = 0.0
    for index, qty_paid, qty_free, unit_price in purchase_list:
        total_taken = qty_paid + qty_free
        item_total_cost = qty_paid * unit_price
        grand_total += item_total_cost
        receipt_lines.append(f"{names[index]:<20} {brands[index]:<15} {qty_paid:>5} {qty_free:>5} {total_taken:>5} {unit_price:>10.2f} {item_total_cost:>10.2f}")
    
    receipt_lines.append("-" * 75)
    # Calculate VAT at 13%
    vat_amount = grand_total * 0.13
    total_with_vat = grand_total + vat_amount
    
    receipt_lines.append(f"SUBTOTAL: NPR {grand_total:>10.2f}")
    receipt_lines.append(f"VAT (13%): NPR {vat_amount:>10.2f}")
    receipt_lines.append(f"GRAND TOTAL: NPR {total_with_vat:>10.2f}")
    receipt_lines.append("\nThank you for shopping at WeCare!")
    
    receipt_filename = create_receipt_filename("CUST")
    record_receipt(receipt_filename, "\n".join(receipt_lines))
    
    return receipt_filename, total_with_vat

def create_supplier_invoice(supplier, restock_details):
    """Creates and saves a supplier restock invoice."""
    invoice_lines = []
    invoice_lines.append("=== WeCare Supplier Invoice ===")
    invoice_lines.append(f"Supplier: {supplier}")
    invoice_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    invoice_lines.append("\nItems Received:")
    invoice_lines.append(f"{'Item':<20} {'Brand':<15} {'Quantity':>10} {'Unit Cost':>10} {'Total Cost':>12}")
    invoice_lines.append("-" * 75)
    
    total_restock_cost = 0
    for index, name, brand, origin, qty, cost in restock_details:
        item_total = qty * cost
        total_restock_cost += item_total
        invoice_lines.append(f"{name:<20} {brand:<15} {qty:>10} {cost:>10} {item_total:>12}")
    
    invoice_lines.append("-" * 75)
    # Calculate VAT at 13%
    vat_amount = total_restock_cost * 0.13
    total_with_vat = total_restock_cost + vat_amount
    
    invoice_lines.append(f"SUBTOTAL: NPR {total_restock_cost:>12}")
    invoice_lines.append(f"VAT (13%): NPR {vat_amount:>12}")
    invoice_lines.append(f"TOTAL COST: NPR {total_with_vat:>12}")
    
    invoice_filename = create_receipt_filename("SUPP")
    record_receipt(invoice_filename, "\n".join(invoice_lines))
    
    return invoice_filename, total_with_vat