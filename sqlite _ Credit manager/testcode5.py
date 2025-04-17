from mainlogic import MainLogic

def test_main_logic_methods_set_5():
    print("---- Testing MainLogic Methods (Set 5) ----")

    # 1. Test bulk_add_customers
    print("\nTest: bulk_add_customers")
    customers = [
        {"customer_name": "Alice Johnson", "amount_credited": 150.00, "address": "789 Elm St", "phone": "1234567890", "email": "alice@example.com", "promised_date": "2025-04-20"},
        {"customer_name": "Bob Smith", "amount_credited": 200.00, "address": "456 Oak St", "phone": "9876543210", "email": "bob@example.com", "promised_date": "2025-05-01"},
    ]
    result = MainLogic.bulk_add_customers(customers)
    print(result)
    '''
    Expected Output:
    - If successful: "Bulk customer addition completed successfully."
    - On error: "Error in bulk customer addition: <error_message>"
    '''

    # 2. Test bulk_add_credits
    print("\nTest: bulk_add_credits")
    credits = [
        {"customer_id": "2025040101", "amount_credited": 300.00, "date_credited": "2025-04-15"},
        {"customer_id": "2025040102", "amount_credited": 400.00, "date_credited": "2025-04-16"},
    ]
    result = MainLogic.bulk_add_credits(credits)
    print(result)
    '''
    Expected Output:
    - If successful: "Bulk credit addition completed successfully."
    - On error: "Error in bulk credit addition: <error_message>"
    '''

    # 3. Test bulk_add_payments
    print("\nTest: bulk_add_payments")
    payments = [
        {"customer_id": "2025040101", "amount_paid": 100.00, "date_paid": "2025-04-17"},
        {"customer_id": "2025040102", "amount_paid": 200.00, "date_paid": "2025-04-18"},
    ]
    result = MainLogic.bulk_add_payments(payments)
    print(result)
    '''
    Expected Output:
    - If successful: "Bulk payment addition completed successfully."
    - On error: "Error in bulk payment addition: <error_message>"
    '''

    # 4. Test fetch_customer_data_by_criteria
    print("\nTest: fetch_customer_data_by_criteria")
    result = MainLogic.fetch_customer_data_by_criteria(email="alice@example.com")
    print("Customer Data by Criteria (Email: alice@example.com):", result)
    '''
    Expected Output:
    - If successful: List of matching customers based on the criteria (e.g., [{"customer_id": "2025040103", ...}]).
    - If no matches found: "No matching customers found."
    - On error: "Error fetching customer data by criteria: <error_message>"
    '''

    # 5. Test generate_report
    print("\nTest: generate_report")
    report = MainLogic.generate_report()
    print("Generated Report:", report)
    '''
    Expected Output:
    - If successful: A dictionary summarizing the total customers, total credited, total paid, and total pending amounts (e.g., {"total_customers": 2, "total_credited": 1000.00, "total_paid": 800.00, "total_pending": 200.00}).
    - On error: "Error generating report: <error_message>"
    '''

    # 6. Test reset_database
    print("\nTest: reset_database")
    reset_result = MainLogic.reset_database()
    print(reset_result)
    '''
    Expected Output:
    - If successful: "Database reset successfully."
    - On error: "Error resetting database: <error_message>"
    '''

# Run the tests
if __name__ == "__main__":
    test_main_logic_methods_set_5()
