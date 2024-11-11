import os
import json

# --- Constants for file paths ---
USER_FILE = 'users.txt'
PRODUCT_FILE = 'products.txt'

# --- Utility functions for file handling ---
def load_data(file):
    """Load data from a file if it exists, else return an empty dictionary."""
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    """Save data to a file."""
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# --- User Authentication & Role Management ---
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {"username": self.username, "password": self.password, "role": self.role}

class UserManager:
    def __init__(self):
        self.users = load_data(USER_FILE)

    def add_user(self, username, password, role):
        if username in self.users:
            raise ValueError("User already exists.")
        self.users[username] = User(username, password, role).to_dict()
        save_data(USER_FILE, self.users)

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == password:
            return User(user["username"], user["password"], user["role"])
        else:
            raise ValueError("Invalid username or password.")

# --- Product Management (OOP Concepts) ---
class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock_quantity": self.stock_quantity
        }

class InventoryManager:
    LOW_STOCK_THRESHOLD = 5

    def __init__(self):
        self.products = load_data(PRODUCT_FILE)

    def add_product(self, product_id, name, category, price, stock_quantity):
        if product_id in self.products:
            raise ValueError("Product ID already exists.")
        product = Product(product_id, name, category, price, stock_quantity)
        self.products[product_id] = product.to_dict()
        save_data(PRODUCT_FILE, self.products)

    def update_product(self, product_id, name=None, category=None, price=None, stock_quantity=None):
        product = self.products.get(product_id)
        if not product:
            raise ValueError("Product not found.")
        if name:
            product["name"] = name
        if category:
            product["category"] = category
        if price is not None:
            product["price"] = price
        if stock_quantity is not None:
            product["stock_quantity"] = stock_quantity
        self.products[product_id] = product
        save_data(PRODUCT_FILE, self.products)

    def delete_product(self, product_id):
        if product_id not in self.products:
            raise ValueError("Product not found.")
        del self.products[product_id]
        save_data(PRODUCT_FILE, self.products)

    def view_product(self, product_id):
        product = self.products.get(product_id)
        if product:
            return product
        else:
            raise ValueError("Product not found.")

    def view_all_products(self):
        return self.products.values()

    def search_products(self, name=None, category=None):
        results = [
            product for product in self.products.values()
            if (name and name.lower() in product["name"].lower()) or
               (category and category.lower() in product["category"].lower())
        ]
        return results

    def adjust_stock(self, product_id, amount):
        product = self.products.get(product_id)
        if not product:
            raise ValueError("Product not found.")
        product["stock_quantity"] += amount
        if product["stock_quantity"] < InventoryManager.LOW_STOCK_THRESHOLD:
            print(f"Warning: Low stock for {product['name']}. Consider restocking.")
        save_data(PRODUCT_FILE, self.products)

# --- Role-Based Access and Console Menu ---
class InventoryManagementSystem:
    def __init__(self):
        self.user_manager = UserManager()
        self.inventory_manager = InventoryManager()
        self.current_user = None

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        try:
            self.current_user = self.user_manager.authenticate(username, password)
            print(f"Welcome, {self.current_user.username}!")
        except ValueError as e:
            print(e)

    def run(self):
        while not self.current_user:
            self.login()
        while True:
            self.display_menu()
            choice = input("Choose an option: ")
            if choice == "1" and self.current_user.role == "Admin":
                self.add_user()
            elif choice == "2" and self.current_user.role == "Admin":
                self.add_product()
            elif choice == "3" and self.current_user.role == "Admin":
                self.update_product()
            elif choice == "4" and self.current_user.role == "Admin":
                self.delete_product()
            elif choice == "5":
                self.view_product()
            elif choice == "6":
                self.view_all_products()
            elif choice == "7":
                self.search_product()
            elif choice == "8" and self.current_user.role == "Admin":
                self.adjust_stock()
            elif choice == "0":
                print("Exiting system.")
                break
            else:
                print("Invalid choice or access denied.")

    def display_menu(self):
        print("\nInventory Management System")
        if self.current_user.role == "Admin":
            print("1. Add User")
            print("2. Add Product")
            print("3. Update Product")
            print("4. Delete Product")
        print("5. View Product")
        print("6. View All Products")
        print("7. Search Product")
        if self.current_user.role == "Admin":
            print("8. Adjust Stock")
        print("0. Exit")

    def add_user(self):
        username = input("Enter new username: ")
        password = input("Enter new password: ")
        role = input("Enter role (Admin/User): ")
        try:
            self.user_manager.add_user(username, password, role)
            print("User added successfully.")
        except ValueError as e:
            print(e)

    def add_product(self):
        product_id = input("Enter Product ID: ")
        name = input("Enter Product Name: ")
        category = input("Enter Category: ")
        price = float(input("Enter Price: "))
        stock_quantity = int(input("Enter Stock Quantity: "))
        try:
            self.inventory_manager.add_product(product_id, name, category, price, stock_quantity)
            print("Product added successfully.")
        except ValueError as e:
            print(e)

    def update_product(self):
        product_id = input("Enter Product ID: ")
        name = input("Enter New Product Name (or leave blank): ")
        category = input("Enter New Category (or leave blank): ")
        price = input("Enter New Price (or leave blank): ")
        stock_quantity = input("Enter New Stock Quantity (or leave blank): ")
        try:
            self.inventory_manager.update_product(
                product_id, 
                name=name if name else None, 
                category=category if category else None,
                price=float(price) if price else None,
                stock_quantity=int(stock_quantity) if stock_quantity else None
            )
            print("Product updated successfully.")
        except ValueError as e:
            print(e)

    def delete_product(self):
        product_id = input("Enter Product ID to delete: ")
        try:
            self.inventory_manager.delete_product(product_id)
            print("Product deleted successfully.")
        except ValueError as e:
            print(e)

    def view_product(self):
        product_id = input("Enter Product ID: ")
        try:
            product = self.inventory_manager.view_product(product_id)
            print(product)
        except ValueError as e:
            print(e)

    def view_all_products(self):
        products = self.inventory_manager.view_all_products()
        for product in products:
            print(product)

    def search_product(self):
        name = input("Enter name to search (or leave blank): ")
        category = input("Enter category to search (or leave blank): ")
        results = self.inventory_manager.search_products(
            name=name if name else None,
            category=category if category else None
        )
        for product in results:
            print(product)

    def adjust_stock(self):
        product_id = input("Enter Product ID to adjust stock: ")
        amount = int(input("Enter amount to adjust (negative to reduce): "))
        try:
            self.inventory_manager.adjust_stock(product_id, amount)
            print("Stock adjusted successfully.")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    ims = InventoryManagementSystem()
    ims.run()
