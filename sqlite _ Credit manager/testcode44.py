from example import MainLogic

def test_main_logic_methods_set_4():
    print("---- Testing MainLogic Methods (Set 4) ----")

    # 1. Test filter_credits_by_date
    print("\nTest: filter_credits_by_date")
    credits = MainLogic.filter_credits_by_date("2025-04-01", "2025-04-30")
    print("Filtered Credits (April 2025):", credits)
    '''
    Expected Output:
    - If successful: List of tuples containing credit records for the specified date range (e.g., [("2025-04-15", 200.00), ...]).
    - If no credits exist in the range: An empty list [].
    - On error: "Error filtering credits by date range (2025-04-01 to 2025-04-30): <error_message>"
    '''

    # 2. Test filter_payments_by_date
    print("\nTest: filter_payments_by_date")
    payments = MainLogic.filter_payments_by_date("2025-04-01", "2025-04-30")
    print("Filtered Payments (April 2025):", payments)
    '''
    Expected Output:
    - If successful: List of tuples containing payment records for the specified date range (e.g., [("2025-04-16", 100.00), ...]).
    - If no payments exist in the range: An empty list [].
    - On error: "Error filtering payments by date range (2025-04-01 to 2025-04-30): <error_message>"
    '''

    # 3. Test fetch_total_credited
    print("\nTest: fetch_total_credited")
    total_credited = MainLogic.fetch_total_credited()
    print("Total Credited (All Customers):", total_credited)
    '''
    Expected Output:
    - If successful: "Total credited across all customers: <total_amount>."
    - If an error occurs: "Error fetching total credited: <error_message>"
    '''

    # 4. Test fetch_total_credited (Specific Customer)
    print("\nTest: fetch_total_credited (Specific Customer)")
    total_credited_customer = MainLogic.fetch_total_credited(customer_id="2025040101")  # Use a valid customer ID
    print("Total Credited (Customer ID: 2025040101):", total_credited_customer)
    '''
    Expected Output:
    - If successful: "Total credited for Customer ID '2025040101': <total_amount>."
    - If no credits exist for the customer: "Total credited for Customer ID '2025040101': 0.00."
    - On error: "Error fetching total credited: <error_message>"
    '''

    # 5. Test fetch_total_paid
    print("\nTest: fetch_total_paid")
    total_paid = MainLogic.fetch_total_paid()
    print("Total Paid (All Customers):", total_paid)
    '''
    Expected Output:
    - If successful: "Total paid across all customers: <total_amount>."
    - If an error occurs: "Error fetching total paid: <error_message>"
    '''

    # 6. Test fetch_total_paid (Specific Customer)
    print("\nTest: fetch_total_paid (Specific Customer)")
    total_paid_customer = MainLogic.fetch_total_paid(customer_id="2025040101")  # Use a valid customer ID
    print("Total Paid (Customer ID: 2025040101):", total_paid_customer)
    '''
    Expected Output:
    - If successful: "Total paid for Customer ID '2025040101': <total_amount>."
    - If no payments exist for the customer: "Total paid for Customer ID '2025040101': 0.00."
    - On error: "Error fetching total paid: <error_message>"
    '''

    # 7. Test fetch_customer_ids
    print("\nTest: fetch_customer_ids")
    customer_ids = MainLogic.fetch_customer_ids()
    print("Customer IDs:", customer_ids)
    '''
    Expected Output:
    - If successful: List of customer IDs (e.g., ["2025040101", "2025040102", ...]).
    - If no customers exist: An empty list [].
    - On error: "Error fetching customer IDs: <error_message>"
    '''

    # 8. Test get_dashboard_summary
    print("\nTest: get_dashboard_summary")
    dashboard_summary = MainLogic.get_dashboard_summary()
    print("Dashboard Summary:", dashboard_summary)
    '''
    Expected Output:
    - If successful: A dictionary containing "total_credited", "total_paid", and "total_pending" (e.g., {"total_credited": 500.00, "total_paid": 300.00, "total_pending": 200.00}).
    - On error: "Error generating dashboard summary: <error_message>"
    '''

# Run the tests
if __name__ == "__main__":
    test_main_logic_methods_set_4()
