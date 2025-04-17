from mainlogic import MainLogic

def test_main_logic_methods_set_3():
    print("---- Testing MainLogic Methods (Set 3) ----")

    # 1. Test fetch_all_records
    print("\nTest: fetch_all_records")
    all_records = MainLogic.fetch_all_records()
    print("All Records:", all_records)
    '''
    Expected Output:
    - If successful: List of tuples containing all customer records along with credit, payment, and pending amount details.
    - If no records exist: An appropriate message or empty list [].
    - On error: "Error fetching all records: <error_message>"
    '''

    # 2. Test fetch_paid_customers
    print("\nTest: fetch_paid_customers")
    paid_customers = MainLogic.fetch_paid_customers()
    print("Paid Customers:", paid_customers)
    '''
    Expected Output:
    - If successful: List of customers who have made payments (e.g., [{"customer_id": "2025040101", "name": "John Doe", ...}]).
    - If no customers have made payments: An empty list [].
    - On error: "Error fetching paid customers: <error_message>"
    '''

    # 3. Test fetch_not_paid_records
    print("\nTest: fetch_not_paid_records")
    not_paid_records = MainLogic.fetch_not_paid_records()
    print("Not Paid Records:", not_paid_records)
    '''
    Expected Output:
    - If successful: List of customers with credits but no payments (e.g., [{"customer_id": "2025040102", "name": "Jane Doe", ...}]).
    - If all customers have made payments: An empty list [].
    - On error: "Error fetching not paid records: <error_message>"
    '''

    # 4. Test get_customer_summary_by_name
    print("\nTest: get_customer_summary_by_name")
    customer_name_summary = MainLogic.get_customer_summary_by_name("John Doe")
    print("Customer Summary by Name (John Doe):", customer_name_summary)
    '''
    Expected Output:
    - If successful: List of dictionaries containing summaries for all customers matching the name "John Doe".
    - If no customer matches the name: "No customer found with name 'John Doe'."
    - On error: "Error fetching summary for customer name 'John Doe': <error_message>"
    '''

    # 5. Test get_credit_info_for_display
    print("\nTest: get_credit_info_for_display")
    credit_info = MainLogic.get_credit_info_for_display(customer_id="2025040101")  # Use a valid customer ID
    print("Credit Info for Display:", credit_info)
    '''
    Expected Output:
    - If successful: Tuple with dates and total credited amounts for the customer (e.g., ("2025-04-15,2025-04-20", 400.00)).
    - If no credits exist for the customer: ("", 0).
    - On error: "Error fetching credit info for customer ID '2025040101': <error_message>"
    '''

    # 6. Test get_payment_info_for_display
    print("\nTest: get_payment_info_for_display")
    payment_info = MainLogic.get_payment_info_for_display(customer_id="2025040101")  # Use a valid customer ID
    print("Payment Info for Display:", payment_info)
    '''
    Expected Output:
    - If successful: Tuple with dates and total paid amounts for the customer (e.g., ("2025-04-16", 100.00)).
    - If no payments exist for the customer: ("", 0).
    - On error: "Error fetching payment info for customer ID '2025040101': <error_message>"
    '''

# Run the tests
if __name__ == "__main__":
    test_main_logic_methods_set_3()