import sqlite3
from db_utility import DBUtility as db

class CheckPayment:
    @staticmethod
    def find_pending_amount(customer_id):
        """
        Find the pending amount for a given customer.

        Parameters:
        - customer_id: The ID of the customer.

        Returns:
        - Pending amount (credited - paid).
        """
        try:
            credited = db.fetch_total("amount_credited", "Credits", f"customer_id = '{customer_id}'")
            paid = db.fetch_total("amount_paid", "PayCredits", f"customer_id = '{customer_id}'")
            return credited - paid
        except Exception as e:
            print(f"Error finding pending amount for customer {customer_id}: {e}")
            return 0.0

    @staticmethod
    def find_not_paid_customers():
        """
        Find customers who have credits but no payments.

        Returns:
        - List of customer IDs who haven't made any payments.
        """
        try:
            credited_customers = db.fetch_unique_values("customer_id", "Credits")
            paid_customers = db.fetch_unique_values("customer_id", "PayCredits")
            not_paid_customers = list(set(credited_customers) - set(paid_customers))
            return not_paid_customers
        except Exception as e:
            print(f"Error finding not-paid customers: {e}")
            return []

    @staticmethod
    def get_customer_history(customer_id):
        """
        Get credit and payment history for a specific customer.

        Parameters:
        - customer_id: The ID of the customer.

        Returns:
        - A dictionary containing credits and payments as lists of tuples.
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()

                # Fetch credit history
                credit_query = '''
                    SELECT date_credited, amount_credited
                    FROM Credits
                    WHERE customer_id = ?
                '''
                cursor.execute(credit_query, (customer_id,))
                credit_history = cursor.fetchall()

                # Fetch payment history
                payment_query = '''
                    SELECT date_paid, amount_paid
                    FROM PayCredits
                    WHERE customer_id = ?
                '''
                cursor.execute(payment_query, (customer_id,))
                payment_history = cursor.fetchall()

                return {
                    "credits": credit_history,
                    "payments": payment_history
                }
        except sqlite3.Error as e:
            print(f"Error retrieving history for customer {customer_id}: {e}")
            return {"credits": [], "payments": []}


# Test Code
if __name__ == "__main__":
    try:
        # Test pending amount
        pending_amount = CheckPayment.find_pending_amount("2025040301")
        print(f"Pending amount for customer 2025040301: {pending_amount:.2f}")

        # Test finding not-paid customers
        not_paid_customers = CheckPayment.find_not_paid_customers()
        print(f"Customers who have not paid: {not_paid_customers}")

        # Test customer history
        customer_history = CheckPayment.get_customer_history("2025040301")
        print(f"Credit history for customer 2025040301: {customer_history['credits']}")
        print(f"Payment history for customer 2025040301: {customer_history['payments']}")
    except Exception as e:
        print(f"An error occurred during testing: {e}")