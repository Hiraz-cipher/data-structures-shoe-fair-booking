from datetime import datetime
from typing import Dict, List, Optional

# ============================================================
#   DATA STRUCTURE CLASSES
# ============================================================

class ItemRecord:
    """Represents a shoe item in the catalog."""

    def __init__(self, item_code: str, item_name: str, unit_price: float):
        # Initialize item attributes
        self.item_code = item_code
        self.item_name = item_name
        self.unit_price = unit_price

    def __str__(self):
        # String representation for displaying catalog items
        return f"{self.item_code} - {self.item_name}: LKR {self.unit_price:,.2f}"


class OrderItemRecord:
    """Represents an individual item entry within an order."""

    def __init__(self, item_code: str, item_name: str, unit_price: float, quantity: int):
        self.item_code = item_code
        self.item_name = item_name
        self.unit_price = unit_price
        self.quantity = quantity
        self.subtotal = unit_price * quantity  # subtotal = price × quantity

    def update_quantity(self, new_quantity: int):
        """Update item quantity and recalculate subtotal."""
        self.quantity = new_quantity
        self.subtotal = self.unit_price * self.quantity

    def __str__(self):
        # Print friendly version of the order item details
        return f"{self.quantity} × {self.item_name} @ LKR {self.unit_price:,.2f} = LKR {self.subtotal:,.2f}"


class OrderRecord:
    """Represents a complete customer order with multiple items."""

    def __init__(self, order_number: str, customer_name: str,
                 contact_number: str, payment_method: str):
        # Basic order details
        self.order_number = order_number
        self.customer_name = customer_name
        self.contact_number = contact_number
        self.order_date_time = datetime.now()  # record creation time

        # List to hold all items for this order
        self.items: List[OrderItemRecord] = []

        # Financial details
        self.subtotal = 0.0
        self.payment_method = payment_method  # either "Online" or "On-site"
        self.processing_fee = 0.0
        self.total_bill = 0.0
        self.payment_status = "Pending"  # initially pending

    def calculate_total(self):
        """Compute subtotal, processing fee, and total payable amount."""
        # Calculate subtotal from item subtotals
        self.subtotal = sum(item.subtotal for item in self.items)

        # Add a 3% processing fee only for online payments
        if self.payment_method == "Online":
            self.processing_fee = self.subtotal * 0.03
        else:
            self.processing_fee = 0.0

        # Calculate the final total
        self.total_bill = self.subtotal + self.processing_fee
        return self.total_bill


class OrderNumberGenerator:
    """Generates unique sequential order numbers with prefix and year."""

    def __init__(self, prefix: str = "CSF", year: int = 2025):
        self.prefix = prefix
        self.year = year
        self.counter = 0  # keeps track of how many orders have been generated

    def generate_next(self) -> str:
        """Generate the next sequential order number."""
        self.counter += 1
        return f"{self.prefix}{self.year}{self.counter:06d}"

    def get_current(self) -> str:
        """Return the most recently generated order number."""
        return f"{self.prefix}{self.year}{self.counter:06d}"


class RevenueSummary:
    """Tracks system-wide revenue and order statistics."""

    def __init__(self):
        # Cumulative financial statistics
        self.total_orders = 0
        self.online_payment_count = 0
        self.onsite_payment_count = 0
        self.total_revenue = 0.0
        self.total_processing_fees = 0.0
        self.net_revenue = 0.0

    def update(self, order: OrderRecord):
        """Update revenue metrics after an order is completed."""
        self.total_orders += 1
        self.total_revenue += order.total_bill
        self.total_processing_fees += order.processing_fee

        # Count by payment method
        if order.payment_method == "Online":
            self.online_payment_count += 1
        else:
            self.onsite_payment_count += 1

        # Net revenue = total - fees
        self.net_revenue = self.total_revenue - self.total_processing_fees


# ============================================================
#   ALGORITHM 1: INITIALIZE SYSTEM
# ============================================================

def initialize_system():
    """
    Initialize all key data structures:
      - Item catalog
      - Orders database
      - Order number generator
      - Revenue summary
    """
    # Create catalog of available shoes
    item_catalog: Dict[str, ItemRecord] = {
        "S001": ItemRecord("S001", "Men's Leather Shoes", 5500.00),
        "S002": ItemRecord("S002", "Women's Heels", 4000.00),
        "S003": ItemRecord("S003", "Casual Sneakers", 3200.00),
        "S004": ItemRecord("S004", "Children's Sandals", 2000.00),
        "S005": ItemRecord("S005", "Running Shoes", 4800.00),
        "S006": ItemRecord("S006", "Flip-Flops", 1200.00)
    }

    # Dictionary to store all orders using order_number as key
    orders_database: Dict[str, OrderRecord] = {}

    # Order number generator (sequential)
    order_generator = OrderNumberGenerator()

    # Revenue summary tracker
    revenue_summary = RevenueSummary()

    return item_catalog, orders_database, order_generator, revenue_summary


# ============================================================
#   ALGORITHM 2: DISPLAY MENU
# ============================================================

def display_menu(item_catalog: Dict[str, ItemRecord]):
    """Display the available shoe catalog with prices."""
    print("\n" + "=" * 60)
    print("           COLOMBO SHOE FAIR - MENU")
    print("=" * 60)
    print(f"{'Code':<8} {'Item Name':<30} {'Price (LKR)':>15}")
    print("-" * 60)

    # Loop through each item and print its details
    for item in item_catalog.values():
        print(f"{item.item_code:<8} {item.item_name:<30} {item.unit_price:>15,.2f}")

    print("=" * 60)


# ============================================================
#   ALGORITHM 3: CREATE NEW ORDER
# ============================================================

def create_new_order(customer_name: str, contact_number: str,
                     payment_method: str, order_generator: OrderNumberGenerator) -> Optional[OrderRecord]:
    """
    Create a new customer order record.
    Returns an OrderRecord object if successful, otherwise None.
    """
    # Input validation
    if not customer_name.strip():
        print("Error: Customer name cannot be empty!")
        return None

    if not contact_number.strip():
        print("Error: Contact number cannot be empty!")
        return None

    if payment_method not in ["Online", "On-site"]:
        print("Error: Payment method must be 'Online' or 'On-site'!")
        return None

    # Generate a new unique order number
    order_number = order_generator.generate_next()

    # Create the order object
    new_order = OrderRecord(order_number, customer_name, contact_number, payment_method)

    print(f"\nOrder created successfully!")
    print(f"Order Number: {order_number}")
    print(f"Customer: {customer_name}")
    print(f"Payment Method: {payment_method}")

    return new_order


# ============================================================
#   ALGORITHM 4: ADD ITEM TO ORDER
# ============================================================

def add_item_to_order(order: OrderRecord, item_code: str, quantity: int,
                      item_catalog: Dict[str, ItemRecord]) -> bool:
    """
    Add an item to a specific order.
    Returns True if successful, otherwise False.
    """
    # Validate quantity
    if quantity <= 0:
        print("Error: Quantity must be positive!")
        return False

    # Check if item exists
    if item_code not in item_catalog:
        print(f"Error: Item code '{item_code}' not found in catalog!")
        return False

    # Retrieve item details
    item_details = item_catalog[item_code]

    # Check if item already in order; if yes, update quantity
    existing_item = None
    for item in order.items:
        if item.item_code == item_code:
            existing_item = item
            break

    if existing_item:
        # Increase quantity if already added
        new_quantity = existing_item.quantity + quantity
        existing_item.update_quantity(new_quantity)
        print(f"Updated: {item_details.item_name} - New quantity: {new_quantity}")
    else:
        # Otherwise, add as a new order line
        order_item = OrderItemRecord(
            item_code,
            item_details.item_name,
            item_details.unit_price,
            quantity
        )
        order.items.append(order_item)
        print(f"Added: {quantity} × {item_details.item_name}")

    # Recalculate total after changes
    order.calculate_total()

    return True


# ============================================================
#   ALGORITHM 7: SEARCH ORDER
# ============================================================

def search_order(order_number: str, orders_database: Dict[str, OrderRecord]) -> Optional[OrderRecord]:
    """
    Look up an order by number and print full details.
    Returns the order object if found, otherwise None.
    """
    order = orders_database.get(order_number)

    if not order:
        print(f"\nOrder '{order_number}' not found!")
        return None

    # Display order summary
    print("\n" + "=" * 60)
    print("                   ORDER DETAILS")
    print("=" * 60)
    print(f"Order Number:      {order.order_number}")
    print(f"Customer Name:     {order.customer_name}")
    print(f"Contact Number:    {order.contact_number}")
    print(f"Order Date/Time:   {order.order_date_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Payment Method:    {order.payment_method}")
    print(f"Payment Status:    {order.payment_status}")
    print("-" * 60)
    print("ITEMS ORDERED:")
    print("-" * 60)

    # Print each item
    for item in order.items:
        print(f"  {item}")

    # Totals
    print("-" * 60)
    print(f"Subtotal:          LKR {order.subtotal:>12,.2f}")
    print(f"Processing Fee:    LKR {order.processing_fee:>12,.2f}")
    print(f"TOTAL BILL:        LKR {order.total_bill:>12,.2f}")
    print("=" * 60)

    return order


# ============================================================
#   ALGORITHM 8: ADD ITEMS TO EXISTING ON-SITE ORDER
# ============================================================

def add_items_to_existing_order(order_number: str, orders_database: Dict[str, OrderRecord],
                                item_catalog: Dict[str, ItemRecord]) -> bool:
    """
    Allow adding additional items to an existing on-site (unpaid) order.
    """
    order = orders_database.get(order_number)

    if not order:
        print(f"Error: Order '{order_number}' not found!")
        return False

    # Only on-site unpaid orders are editable
    if order.payment_method == "Online":
        print("Error: Cannot add items to online payment orders!")
        return False

    if order.payment_status == "Completed":
        print("Error: Cannot add items to completed orders!")
        return False

    # Show existing order before modification
    print("\nCurrent order details:")
    search_order(order_number, orders_database)

    # Interactive item addition loop
    print("\nAdding items to order...")
    while True:
        display_menu(item_catalog)

        item_code = input("\nEnter item code to add (or 'done' to finish): ").strip().upper()

        if item_code.lower() == 'done':
            break

        try:
            quantity = int(input("Enter quantity: "))
            add_item_to_order(order, item_code, quantity, item_catalog)
        except ValueError:
            print("Error: Please enter a valid number for quantity!")

    print("\n--- Order Updated Successfully ---")
    search_order(order_number, orders_database)

    return True


# ============================================================
#   ALGORITHM 9: PROCESS PAYMENT
# ============================================================

def process_payment(order_number: str, orders_database: Dict[str, OrderRecord],
                    revenue_summary: RevenueSummary) -> bool:
    """
    Process and mark an order as paid, then update revenue summary.
    """
    order = orders_database.get(order_number)

    if not order:
        print(f"Error: Order '{order_number}' not found!")
        return False

    if order.payment_status == "Completed":
        print("Error: Order already paid!")
        return False

    # Mark as paid
    order.payment_status = "Completed"

    # Update global revenue stats
    revenue_summary.update(order)

    # Display confirmation
    print(f"\n{'=' * 60}")
    print("           PAYMENT PROCESSED SUCCESSFULLY")
    print(f"{'=' * 60}")
    print(f"Order Number:  {order.order_number}")
    print(f"Amount Paid:   LKR {order.total_bill:,.2f}")
    print(f"Payment Type:  {order.payment_method}")
    print(f"{'=' * 60}")

    return True


# ============================================================
#   ALGORITHM 10: CALCULATE TOTAL REVENUE
# ============================================================

def calculate_total_revenue(orders_database: Dict[str, OrderRecord],
                            revenue_summary: RevenueSummary):
    """
    Print a comprehensive revenue report, including totals,
    breakdown by payment type, and pending payments.
    """
    print("\n" + "=" * 60)
    print("        COLOMBO SHOE FAIR - REVENUE REPORT")
    print("=" * 60)
    print(f"Total Orders Completed:     {revenue_summary.total_orders}")
    print("-" * 60)
    print("Payment Method Breakdown:")
    print(f"  Online Payments:          {revenue_summary.online_payment_count}")
    print(f"  On-site Payments:         {revenue_summary.onsite_payment_count}")
    print("-" * 60)
    print("Financial Summary:")
    print(f"  Total Revenue:            LKR {revenue_summary.total_revenue:>12,.2f}")
    print(f"  Processing Fees:          LKR {revenue_summary.total_processing_fees:>12,.2f}")
    print(f"  Net Revenue:              LKR {revenue_summary.net_revenue:>12,.2f}")
    print("=" * 60)

    # Count any pending orders
    pending_count = 0
    pending_amount = 0.0
    for order in orders_database.values():
        if order.payment_status == "Pending":
            pending_count += 1
            pending_amount += order.total_bill

    if pending_count > 0:
        print(f"\nPending Orders:             {pending_count}")
        print(f"Pending Amount:             LKR {pending_amount:,.2f}")
        print("=" * 60)


# ============================================================
#   ALGORITHM 11: MAIN PROGRAM FLOW
# ============================================================

def main():
    """Main user interface and control flow for the program."""
    # Step 1: Initialize all required structures
    item_catalog, orders_database, order_generator, revenue_summary = initialize_system()

    print("\n" + "=" * 60)
    print("   WELCOME TO COLOMBO SHOE FAIR BOOKING SYSTEM")
    print("=" * 60)

    # Continuous main menu loop
    while True:
        print("\n" + "=" * 60)
        print("                    MAIN MENU")
        print("=" * 60)
        print("1. View Available Shoes")
        print("2. Create New Booking")
        print("3. Search Order")
        print("4. Add Items to Existing On-site Order")
        print("5. Process Payment")
        print("6. Generate Revenue Report")
        print("7. Exit")
        print("=" * 60)

        try:
            choice = input("Enter your choice (1-7): ").strip()

            if choice == '1':
                # Display shoe catalog
                display_menu(item_catalog)

            elif choice == '2':
                # Create new booking
                print("\n--- NEW BOOKING ---")
                customer_name = input("Enter customer name: ").strip()
                contact_number = input("Enter contact number: ").strip()

                print("\nPayment Method:")
                print("1. Online (3% processing fee)")
                print("2. On-site (no processing fee)")
                payment_choice = input("Select payment method (1 or 2): ").strip()

                payment_method = "Online" if payment_choice == '1' else "On-site"

                # Create order
                order = create_new_order(customer_name, contact_number,
                                         payment_method, order_generator)

                if order:
                    # Add items to order
                    print("\nAdd items to your order:")
                    while True:
                        display_menu(item_catalog)

                        item_code = input("\nEnter item code (or 'done' to finish): ").strip().upper()

                        if item_code.lower() == 'done':
                            break

                        try:
                            quantity = int(input("Enter quantity: "))
                            add_item_to_order(order, item_code, quantity, item_catalog)
                        except ValueError:
                            print("Error: Please enter a valid number!")

                    # Save and finalize order if it has at least one item
                    if len(order.items) > 0:
                        orders_database[order.order_number] = order
                        print(f"\n--- ORDER SAVED SUCCESSFULLY ---")
                        search_order(order.order_number, orders_database)

                        # Auto-process online payments immediately
                        if order.payment_method == "Online":
                            print("\nProcessing online payment...")
                            process_payment(order.order_number, orders_database,
                                            revenue_summary)
                    else:
                        print("\nOrder cancelled - no items added")

            elif choice == '3':
                # Search existing order
                order_number = input("\nEnter order number: ").strip().upper()
                search_order(order_number, orders_database)

            elif choice == '4':
                # Add more items to on-site order
                order_number = input("\nEnter order number: ").strip().upper()
                add_items_to_existing_order(order_number, orders_database, item_catalog)

            elif choice == '5':
                # Complete payment for a pending order
                order_number = input("\nEnter order number: ").strip().upper()
                process_payment(order_number, orders_database, revenue_summary)

            elif choice == '6':
                # Display full revenue report
                calculate_total_revenue(orders_database, revenue_summary)

            elif choice == '7':
                # Exit program gracefully
                print("\n" + "=" * 60)
                print("  THANK YOU FOR USING COLOMBO SHOE FAIR SYSTEM")
                print("=" * 60)
                break

            else:
                print("\nInvalid choice! Please enter a number between 1 and 7.")

        except KeyboardInterrupt:
            # Graceful exit if user interrupts program
            print("\n\nSystem interrupted. Exiting...")
            break
        except Exception as e:
            # Catch any unexpected runtime errors
            print(f"\nAn error occurred: {e}")
            print("Please try again.")


# ============================================================
#   PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================
#   DATA STRUCTURE CLASSES
# ============================================================

class ItemRecord:
    """Represents a shoe item in the catalog."""

    def __init__(self, item_code: str, item_name: str, unit_price: float):
        # Initialize item attributes
        self.item_code = item_code
        self.item_name = item_name
        self.unit_price = unit_price

    def __str__(self):
        # String representation for displaying catalog items
        return f"{self.item_code} - {self.item_name}: LKR {self.unit_price:,.2f}"


class OrderItemRecord:
    """Represents an individual item entry within an order."""

    def __init__(self, item_code: str, item_name: str, unit_price: float, quantity: int):
        self.item_code = item_code
        self.item_name = item_name
        self.unit_price = unit_price
        self.quantity = quantity
        self.subtotal = unit_price * quantity  # subtotal = price × quantity

    def update_quantity(self, new_quantity: int):
        """Update item quantity and recalculate subtotal."""
        self.quantity = new_quantity
        self.subtotal = self.unit_price * self.quantity

    def __str__(self):
        # Print friendly version of the order item details
        return f"{self.quantity} × {self.item_name} @ LKR {self.unit_price:,.2f} = LKR {self.subtotal:,.2f}"


class OrderRecord:
    """Represents a complete customer order with multiple items."""

    def __init__(self, order_number: str, customer_name: str,
                 contact_number: str, payment_method: str):
        # Basic order details
        self.order_number = order_number
        self.customer_name = customer_name
        self.contact_number = contact_number
        self.order_date_time = datetime.now()  # record creation time

        # List to hold all items for this order
        self.items: List[OrderItemRecord] = []

        # Financial details
        self.subtotal = 0.0
        self.payment_method = payment_method  # either "Online" or "On-site"
        self.processing_fee = 0.0
        self.total_bill = 0.0
        self.payment_status = "Pending"  # initially pending

    def calculate_total(self):
        """Compute subtotal, processing fee, and total payable amount."""
        # Calculate subtotal from item subtotals
        self.subtotal = sum(item.subtotal for item in self.items)

        # Add a 3% processing fee only for online payments
        if self.payment_method == "Online":
            self.processing_fee = self.subtotal * 0.03
        else:
            self.processing_fee = 0.0

        # Calculate the final total
        self.total_bill = self.subtotal + self.processing_fee
        return self.total_bill


class OrderNumberGenerator:
    """Generates unique sequential order numbers with prefix and year."""

    def __init__(self, prefix: str = "CSF", year: int = 2025):
        self.prefix = prefix
        self.year = year
        self.counter = 0  # keeps track of how many orders have been generated

    def generate_next(self) -> str:
        """Generate the next sequential order number."""
        self.counter += 1
        return f"{self.prefix}{self.year}{self.counter:06d}"

    def get_current(self) -> str:
        """Return the most recently generated order number."""
        return f"{self.prefix}{self.year}{self.counter:06d}"


class RevenueSummary:
    """Tracks system-wide revenue and order statistics."""

    def __init__(self):
        # Cumulative financial statistics
        self.total_orders = 0
        self.online_payment_count = 0
        self.onsite_payment_count = 0
        self.total_revenue = 0.0
        self.total_processing_fees = 0.0
        self.net_revenue = 0.0

    def update(self, order: OrderRecord):
        """Update revenue metrics after an order is completed."""
        self.total_orders += 1
        self.total_revenue += order.total_bill
        self.total_processing_fees += order.processing_fee

        # Count by payment method
        if order.payment_method == "Online":
            self.online_payment_count += 1
        else:
            self.onsite_payment_count += 1

        # Net revenue = total - fees
        self.net_revenue = self.total_revenue - self.total_processing_fees


# ============================================================
#   ALGORITHM 1: INITIALIZE SYSTEM
# ============================================================

def initialize_system():
    """
    Initialize all key data structures:
      - Item catalog
      - Orders database
      - Order number generator
      - Revenue summary
    """
    # Create catalog of available shoes
    item_catalog: Dict[str, ItemRecord] = {
        "S001": ItemRecord("S001", "Men's Leather Shoes", 5500.00),
        "S002": ItemRecord("S002", "Women's Heels", 4000.00),
        "S003": ItemRecord("S003", "Casual Sneakers", 3200.00),
        "S004": ItemRecord("S004", "Children's Sandals", 2000.00),
        "S005": ItemRecord("S005", "Running Shoes", 4800.00),
        "S006": ItemRecord("S006", "Flip-Flops", 1200.00)
    }

    # Dictionary to store all orders using order_number as key
    orders_database: Dict[str, OrderRecord] = {}

    # Order number generator (sequential)
    order_generator = OrderNumberGenerator()

    # Revenue summary tracker
    revenue_summary = RevenueSummary()

    return item_catalog, orders_database, order_generator, revenue_summary


# ============================================================
#   ALGORITHM 2: DISPLAY MENU
# ============================================================

def display_menu(item_catalog: Dict[str, ItemRecord]):
    """Display the available shoe catalog with prices."""
    print("\n" + "=" * 60)
    print("           COLOMBO SHOE FAIR - MENU")
    print("=" * 60)
    print(f"{'Code':<8} {'Item Name':<30} {'Price (LKR)':>15}")
    print("-" * 60)

    # Loop through each item and print its details
    for item in item_catalog.values():
        print(f"{item.item_code:<8} {item.item_name:<30} {item.unit_price:>15,.2f}")

    print("=" * 60)


# ============================================================
#   ALGORITHM 3: CREATE NEW ORDER
# ============================================================

def create_new_order(customer_name: str, contact_number: str,
                     payment_method: str, order_generator: OrderNumberGenerator) -> Optional[OrderRecord]:
    """
    Create a new customer order record.
    Returns an OrderRecord object if successful, otherwise None.
    """
    # Input validation
    if not customer_name.strip():
        print("Error: Customer name cannot be empty!")
        return None

    if not contact_number.strip():
        print("Error: Contact number cannot be empty!")
        return None

    if payment_method not in ["Online", "On-site"]:
        print("Error: Payment method must be 'Online' or 'On-site'!")
        return None

    # Generate a new unique order number
    order_number = order_generator.generate_next()

    # Create the order object
    new_order = OrderRecord(order_number, customer_name, contact_number, payment_method)

    print(f"\nOrder created successfully!")
    print(f"Order Number: {order_number}")
    print(f"Customer: {customer_name}")
    print(f"Payment Method: {payment_method}")

    return new_order


# ============================================================
#   ALGORITHM 4: ADD ITEM TO ORDER
# ============================================================

def add_item_to_order(order: OrderRecord, item_code: str, quantity: int,
                      item_catalog: Dict[str, ItemRecord]) -> bool:
    """
    Add an item to a specific order.
    Returns True if successful, otherwise False.
    """
    # Validate quantity
    if quantity <= 0:
        print("Error: Quantity must be positive!")
        return False

    # Check if item exists
    if item_code not in item_catalog:
        print(f"Error: Item code '{item_code}' not found in catalog!")
        return False

    # Retrieve item details
    item_details = item_catalog[item_code]

    # Check if item already in order; if yes, update quantity
    existing_item = None
    for item in order.items:
        if item.item_code == item_code:
            existing_item = item
            break

    if existing_item:
        # Increase quantity if already added
        new_quantity = existing_item.quantity + quantity
        existing_item.update_quantity(new_quantity)
        print(f"Updated: {item_details.item_name} - New quantity: {new_quantity}")
    else:
        # Otherwise, add as a new order line
        order_item = OrderItemRecord(
            item_code,
            item_details.item_name,
            item_details.unit_price,
            quantity
        )
        order.items.append(order_item)
        print(f"Added: {quantity} × {item_details.item_name}")

    # Recalculate total after changes
    order.calculate_total()

    return True


# ============================================================
#   ALGORITHM 7: SEARCH ORDER
# ============================================================

def search_order(order_number: str, orders_database: Dict[str, OrderRecord]) -> Optional[OrderRecord]:
    """
    Look up an order by number and print full details.
    Returns the order object if found, otherwise None.
    """
    order = orders_database.get(order_number)

    if not order:
        print(f"\nOrder '{order_number}' not found!")
        return None

    # Display order summary
    print("\n" + "=" * 60)
    print("                   ORDER DETAILS")
    print("=" * 60)
    print(f"Order Number:      {order.order_number}")
    print(f"Customer Name:     {order.customer_name}")
    print(f"Contact Number:    {order.contact_number}")
    print(f"Order Date/Time:   {order.order_date_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Payment Method:    {order.payment_method}")
    print(f"Payment Status:    {order.payment_status}")
    print("-" * 60)
    print("ITEMS ORDERED:")
    print("-" * 60)

    # Print each item
    for item in order.items:
        print(f"  {item}")

    # Totals
    print("-" * 60)
    print(f"Subtotal:          LKR {order.subtotal:>12,.2f}")
    print(f"Processing Fee:    LKR {order.processing_fee:>12,.2f}")
    print(f"TOTAL BILL:        LKR {order.total_bill:>12,.2f}")
    print("=" * 60)

    return order


# ============================================================
#   ALGORITHM 8: ADD ITEMS TO EXISTING ON-SITE ORDER
# ============================================================

def add_items_to_existing_order(order_number: str, orders_database: Dict[str, OrderRecord],
                                item_catalog: Dict[str, ItemRecord]) -> bool:
    """
    Allow adding additional items to an existing on-site (unpaid) order.
    """
    order = orders_database.get(order_number)

    if not order:
        print(f"Error: Order '{order_number}' not found!")
        return False

    # Only on-site unpaid orders are editable
    if order.payment_method == "Online":
        print("Error: Cannot add items to online payment orders!")
        return False

    if order.payment_status == "Completed":
        print("Error: Cannot add items to completed orders!")
        return False

    # Show existing order before modification
    print("\nCurrent order details:")
    search_order(order_number, orders_database)

    # Interactive item addition loop
    print("\nAdding items to order...")
    while True:
        display_menu(item_catalog)

        item_code = input("\nEnter item code to add (or 'done' to finish): ").strip().upper()

        if item_code.lower() == 'done':
            break

        try:
            quantity = int(input("Enter quantity: "))
            add_item_to_order(order, item_code, quantity, item_catalog)
        except ValueError:
            print("Error: Please enter a valid number for quantity!")

    print("\n--- Order Updated Successfully ---")
    search_order(order_number, orders_database)

    return True


# ============================================================
#   ALGORITHM 9: PROCESS PAYMENT
# ============================================================

def process_payment(order_number: str, orders_database: Dict[str, OrderRecord],
                    revenue_summary: RevenueSummary) -> bool:
    """
    Process and mark an order as paid, then update revenue summary.
    """
    order = orders_database.get(order_number)

    if not order:
        print(f"Error: Order '{order_number}' not found!")
        return False

    if order.payment_status == "Completed":
        print("Error: Order already paid!")
        return False

    # Mark as paid
    order.payment_status = "Completed"

    # Update global revenue stats
    revenue_summary.update(order)

    # Display confirmation
    print(f"\n{'=' * 60}")
    print("           PAYMENT PROCESSED SUCCESSFULLY")
    print(f"{'=' * 60}")
    print(f"Order Number:  {order.order_number}")
    print(f"Amount Paid:   LKR {order.total_bill:,.2f}")
    print(f"Payment Type:  {order.payment_method}")
    print(f"{'=' * 60}")

    return True


# ============================================================
#   ALGORITHM 10: CALCULATE TOTAL REVENUE
# ============================================================

def calculate_total_revenue(orders_database: Dict[str, OrderRecord],
                            revenue_summary: RevenueSummary):
    """
    Print a comprehensive revenue report, including totals,
    breakdown by payment type, and pending payments.
    """
    print("\n" + "=" * 60)
    print("        COLOMBO SHOE FAIR - REVENUE REPORT")
    print("=" * 60)
    print(f"Total Orders Completed:     {revenue_summary.total_orders}")
    print("-" * 60)
    print("Payment Method Breakdown:")
    print(f"  Online Payments:          {revenue_summary.online_payment_count}")
    print(f"  On-site Payments:         {revenue_summary.onsite_payment_count}")
    print("-" * 60)
    print("Financial Summary:")
    print(f"  Total Revenue:            LKR {revenue_summary.total_revenue:>12,.2f}")
    print(f"  Processing Fees:          LKR {revenue_summary.total_processing_fees:>12,.2f}")
    print(f"  Net Revenue:              LKR {revenue_summary.net_revenue:>12,.2f}")
    print("=" * 60)

    # Count any pending orders
    pending_count = 0
    pending_amount = 0.0
    for order in orders_database.values():
        if order.payment_status == "Pending":
            pending_count += 1
            pending_amount += order.total_bill

    if pending_count > 0:
        print(f"\nPending Orders:             {pending_count}")
        print(f"Pending Amount:             LKR {pending_amount:,.2f}")
        print("=" * 60)


# ============================================================
#   ALGORITHM 11: MAIN PROGRAM FLOW
# ============================================================

def main():
    """Main user interface and control flow for the program."""
    # Step 1: Initialize all required structures
    item_catalog, orders_database, order_generator, revenue_summary = initialize_system()

    print("\n" + "=" * 60)
    print("   WELCOME TO COLOMBO SHOE FAIR BOOKING SYSTEM")
    print("=" * 60)

    # Continuous main menu loop
    while True:
        print("\n" + "=" * 60)
        print("                    MAIN MENU")
        print("=" * 60)
        print("1. View Available Shoes")
        print("2. Create New Booking")
        print("3. Search Order")
        print("4. Add Items to Existing On-site Order")
        print("5. Process Payment")
        print("6. Generate Revenue Report")
        print("7. Exit")
        print("=" * 60)

        try:
            choice = input("Enter your choice (1-7): ").strip()

            if choice == '1':
                # Display shoe catalog
                display_menu(item_catalog)

            elif choice == '2':
                # Create new booking
                print("\n--- NEW BOOKING ---")
                customer_name = input("Enter customer name: ").strip()
                contact_number = input("Enter contact number: ").strip()

                print("\nPayment Method:")
                print("1. Online (3% processing fee)")
                print("2. On-site (no processing fee)")
                payment_choice = input("Select payment method (1 or 2): ").strip()

                payment_method = "Online" if payment_choice == '1' else "On-site"

                # Create order
                order = create_new_order(customer_name, contact_number,
                                         payment_method, order_generator)

                if order:
                    # Add items to order
                    print("\nAdd items to your order:")
                    while True:
                        display_menu(item_catalog)

                        item_code = input("\nEnter item code (or 'done' to finish): ").strip().upper()

                        if item_code.lower() == 'done':
                            break

                        try:
                            quantity = int(input("Enter quantity: "))
                            add_item_to_order(order, item_code, quantity, item_catalog)
                        except ValueError:
                            print("Error: Please enter a valid number!")

                    # Save and finalize order if it has at least one item
                    if len(order.items) > 0:
                        orders_database[order.order_number] = order
                        print(f"\n--- ORDER SAVED SUCCESSFULLY ---")
                        search_order(order.order_number, orders_database)

                        # Auto-process online payments immediately
                        if order.payment_method == "Online":
                            print("\nProcessing online payment...")
                            process_payment(order.order_number, orders_database,
                                            revenue_summary)
                    else:
                        print("\nOrder cancelled - no items added")

            elif choice == '3':
                # Search existing order
                order_number = input("\nEnter order number: ").strip().upper()
                search_order(order_number, orders_database)

            elif choice == '4':
                # Add more items to on-site order
                order_number = input("\nEnter order number: ").strip().upper()
                add_items_to_existing_order(order_number, orders_database, item_catalog)

            elif choice == '5':
                # Complete payment for a pending order
                order_number = input("\nEnter order number: ").strip().upper()
                process_payment(order_number, orders_database, revenue_summary)

            elif choice == '6':
                # Display full revenue report
                calculate_total_revenue(orders_database, revenue_summary)

            elif choice == '7':
                # Exit program gracefully
                print("\n" + "=" * 60)
                print("  THANK YOU FOR USING COLOMBO SHOE FAIR SYSTEM")
                print("=" * 60)
                break

            else:
                print("\nInvalid choice! Please enter a number between 1 and 7.")

        except KeyboardInterrupt:
            # Graceful exit if user interrupts program
            print("\n\nSystem interrupted. Exiting...")
            break
        except Exception as e:
            # Catch any unexpected runtime errors
            print(f"\nAn error occurred: {e}")
            print("Please try again.")


# ============================================================
#   PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
