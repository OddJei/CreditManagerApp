from mainlogic import MainLogic

def test_main_logic_methods_set_2():
    print("---- Testing MainLogic Methods (Set 2) ----")

    # 1. Test add_credit_to_customer
    print("\nTest: add_credit_to_customer")
    result = MainLogic.add_credit_to_customer(
        customer_id="2025040101",  # Use a valid customer ID
        amount_credited=200.00,
        date_credited="2025-04-15"
    )
    print(result)
    '''
    Expected Output:
    - If successful: "Credit of 200.00 added successfully to Customer ID '2025040101'."
    - If an error occurs (e.g., invalid customer ID): "Error adding credit to customer ID '2025040101': <error_message>"
    '''

    # 2. Test add_payment_to_customer
    print("\nTest: add_payment_to_customer")
    result = MainLogic.add_payment_to_customer(
        customer_id="2025040101",  # Use a valid customer ID
        amount_paid=100.00,
        date_paid="2025-04-16"
    )
    print(result)
    '''
    Expected Output:
    - If successful: "Payment of 100.00 added successfully to Customer ID '2025040101'."
    - If an error occurs (e.g., invalid customer ID): "Error adding payment to customer ID '2025040101': <error_message>"
    '''

    # 3. Test fetch_pending_amount
    print("\nTest: fetch_pending_amount")
    result = MainLogic.fetch_pending_amount(
        customer_id="2025040101"  # Use a valid customer ID
    )
    print(result)
    '''
    Expected Output:
    - If successful: "Pending amount for Customer ID '2025040101' is 100.00."
    - If an error occurs (e.g., invalid customer ID): "Error fetching pending amount for customer ID '2025040101': <error_message>"
    '''

    # 4. Test fetch_unpaid_customers
    print("\nTest: fetch_unpaid_customers")
    unpaid_customers = MainLogic.fetch_unpaid_customers()
    print("Unpaid Customers:", unpaid_customers)
    '''
    Expected Output:
    - If successful: List of customer IDs who have credits but no payments (e.g., ["2025040102", "2025040103"]).
    - If no unpaid customers: An empty list [].
    - On error: "Error fetching unpaid customers: <error_message>"
    '''

    # 5. Test fetch_credit_history
    print("\nTest: fetch_credit_history")
    credit_history = MainLogic.fetch_credit_history(
        customer_id="2025040101"  # Use a valid customer ID
    )
    print("Credit History:", credit_history)
    '''
    Expected Output:
    - If successful: List of tuples containing credit history for the customer (e.g., [("2025-04-15", 200.00), ...]).
    - If no credits exist for the customer: An empty list [].
    - On error: "Error fetching credit history for customer ID '2025040101': <error_message>"
    '''

    # 6. Test fetch_payment_history
    print("\nTest: fetch_payment_history")
    payment_history = MainLogic.fetch_payment_history(
        customer_id="2025040101"  # Use a valid customer ID
    )
    print("Payment History:", payment_history)
    '''
    Expected Output:
    - If successful: List of tuples containing payment history for the customer (e.g., [("2025-04-16", 100.00), ...]).
    - If no payments exist for the customer: An empty list [].
    - On error: "Error fetching payment history for customer ID '2025040101': <error_message>"
    '''

# Run the tests
if __name__ == "__main__":
    test_main_logic_methods_set_2()
