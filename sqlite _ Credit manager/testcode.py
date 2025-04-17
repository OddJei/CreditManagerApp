from mainlogic import MainLogic

def test_main_logic_methods():
    print("---- Testing MainLogic Methods ----")

    # 1. Test add_customer
    print("\nTest: add_customer")
    result = MainLogic.add_customer(
        customer_fname="Jane",
        customer_lname="Banda",
        customer_mname= "P.",
        address="123 Main St",
        phone="1234517897",
        email="janebanda@example.com",
        promised_date="2025-04-30",
        amount_credited=200
    )
    print(result)
    '''
    Expected Output:
    - If successful: "Customer 'John Doe' successfully added with initial credit of 100.00."
    - If an error occurs (e.g., duplicate customer name, database issue): "Error adding customer: <error_message>"
    '''
"""

    # 2. Test fetch_all_customers
    print("\nTest: fetch_all_customers")
    all_customers = MainLogic.fetch_all_customers()
    if all_customers:
        print("All Customers:")
        for customer in all_customers:
            print(customer)
    else:
        print("No customers found.")
    '''
    Expected Output:
    - If there are records: A list of all customers, each as a tuple containing customer details (e.g., ID, name, address, etc.).
    - If no records exist: "No customers found."
    - On error: "Error fetching customer records: <error_message>"
    '''

    # 3. Test fetch_customer_summary
    print("\nTest: fetch_customer_summary")
    summary = MainLogic.fetch_customer_summary("2025040101")  # Use a valid customer ID
    if "error" not in summary:
        print("Credit History:", summary.get("credits", []))
        print("Payment History:", summary.get("payments", []))
        print("Pending Amount:", summary.get("pending_amount", 0.0))
    else:
        print(summary)
    '''
    Expected Output:
    - If successful: 
      - Credits: List of tuples [(date, amount), ...] for the customer's credit history.
      - Payments: List of tuples [(date, amount), ...] for the customer's payment history.
      - Pending Amount: Float value showing the difference between credited and paid amounts.
    - If an error occurs (e.g., invalid customer ID): "Error fetching summary for customer ID '2025040101': <error_message>"
    '''

    # 4. Test update_customer_details
    print("\nTest: update_customer_details")
    update_result = MainLogic.update_customer_details(
        customer_id="2025040101",  # Use a valid customer ID
        address="456 Elm St",
        phone="9876543210"
    )
    print(update_result)
    '''
    Expected Output:
    - If successful: "Customer ID '2025040101' updated successfully."
    - If an error occurs (e.g., invalid customer ID): "Error updating customer: <error_message>"
    '''

    # 5. Test remove_customer
    print("\nTest: remove_customer")
    remove_result = MainLogic.remove_customer("2025040101")  # Use a valid customer ID
    print(remove_result)
    '''
    Expected Output:
    - If successful: "Customer ID '2025040101' removed successfully."
    - If an error occurs (e.g., invalid customer ID): "Error removing customer: <error_message>"
    '''

    # 6. Test fetch_customer_by_name
    print("\nTest: fetch_customer_by_name")
    customer_name_results = MainLogic.fetch_customer_by_name("John Doe")
    print("Customers with the name 'John Doe':", customer_name_results)
    '''
    Expected Output:
    - If successful: A list of customer IDs matching the name 'John Doe'.
    - If no match exists: An empty list [].
    - On error: "Error fetching customer by name 'John Doe': <error_message>"
    '''


"""
# Run the tests
if __name__ == "__main__":
    test_main_logic_methods()
