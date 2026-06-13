WeCare Beauty Products Inventory System

Overview

This is an inventory management system for a beauty products store called Samu's WeCare. The system helps manage product stock, process customer purchases, handle supplier restocking, and generate sales records.

Features

View All Products - Display all beauty products in stock with details like brand, quantity, and cost

Customer Purchases - Sell products to customers with a special buy 3 get 1 free offer. The system automatically calculates how many free items the customer gets

Supplier Restocking - Add new products to inventory or increase quantities of existing products from suppliers

Automatic Pricing - Products are sold at 200 percent markup on the cost price. The system calculates prices automatically

Receipt Generation - Creates and saves detailed receipts for every customer purchase and supplier transaction

Data Storage - All inventory is saved to a file. Changes are saved automatically after each transaction

File Descriptions

main.py - This is the entry point of the application. It runs the main menu and handles user interactions

operation.py - Contains the main business logic. It handles customer purchases, supplier restocking, and validates customer and supplier names

read.py - Handles reading product data from the file and displaying product information. It also calculates selling prices

write.py - Handles saving data to files and creating receipts for transactions

products.txt - Contains all product information. Each line has product name, brand, quantity, cost, and country of origin

How to Run

1. Make sure Python 3 is installed on your computer
2. Navigate to the program folder
3. Run the command: python main.py
4. Follow the menu options displayed on screen

How to Use

When you run the program, you will see a menu with these options:

1. View Stock - Shows all products available in the store with their details
2. Customer Purchase - Allows a customer to buy products. The customer gets 1 free item for every 3 purchased
3. Supplier Restock - Add new products or increase quantities from suppliers
4. Exit - Closes the program and saves all changes

Product Information

The system stores the following information for each product:

Product Name - Name of the beauty product
Brand - The brand that makes the product
Quantity - How many units are in stock
Cost - The cost price paid to the supplier
Origin - The country where the product is made

Example: Face Wash, Simple brand, 355 units, cost 250, from UK

Special Features

Buy 3 Get 1 Free - When a customer buys 3 items of the same product, they automatically get 1 free item. This is calculated automatically

Automatic Price Calculation - Selling price is always set at 200 percent markup on cost. So if cost is 100, selling price is 300

Name Validation - The system only accepts valid names with letters, spaces, and basic punctuation. Invalid characters are rejected

Receipt Files - Every transaction creates a text file with a timestamp. Customers and suppliers both receive receipts

Error Handling - The system checks for empty inventory, invalid inputs, and insufficient stock before processing transactions

Data Persistence - All inventory changes are saved to the products.txt file automatically after each transaction so no data is lost

