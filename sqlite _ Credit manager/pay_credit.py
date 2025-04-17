from datetime import datetime
from db_utility import DBUtility as db
import sqlite3

class PayCredit:
    def __init__(self, customer_id, amount_paid, date_paid=None):
        self.customer_id = customer_id
        self.date_paid = date_paid if date_paid else datetime.now().strftime("%Y-%m-%d")  # Default to current date
        self.amount_paid = amount_paid
        self.create_table()
        self.validate_customer()

    def create_table(self):
        # Create the PayCredits table if it doesn't exist
        schema = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            date_paid TEXT NOT NULL,
            amount_paid REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        '''
        db.create_table("PayCredits", schema)

    def validate_customer(self):
        # Ensure the customer exists in the Customers table
        existing_customers = db.fetch_unique_values("customer_id", "Customers")
        if self.customer_id not in existing_customers:
            raise ValueError(f"Customer ID {self.customer_id} does not exist in the system.")

    def save_record(self):
        # Save pay credit record to the PayCredits table
        columns = "customer_id, date_paid, amount_paid"
        values = (self.customer_id, self.date_paid, self.amount_paid)
        db.save_record("PayCredits", columns, values)

    @staticmethod
    def sum_amount_paid():
        """
        Fetch the total paid amount from the database.

        Returns:
        - Total paid amount as a float.
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                query = '''
                    SELECT SUM(amount_paid)
                    FROM PayCredits
                '''
                cursor.execute(query)
                return cursor.fetchone()[0] or 0.0
        except sqlite3.Error as e:
            print(f"Error summing paid amounts: {e}")
            return 0.0

    @staticmethod
    def filter_payments_by_date(start_date, end_date):
        """
        Fetch payments within a specific date range.

        Parameters:
        - start_date: Start of the date range (inclusive).
        - end_date: End of the date range (inclusive).

        Returns:
        - List of tuples containing records in the specified date range.
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                query = '''
                    SELECT customer_id, date_paid, amount_paid
                    FROM PayCredits
                    WHERE date_paid BETWEEN ? AND ?
                '''
                cursor.execute(query, (start_date, end_date))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error filtering payments by date: {e}")
            return []


# Test Code
if __name__ == "__main__":
    try:
        # Create a payment record
        payment = PayCredit("2025041201", 50.00)  # Customer ID and payment amount
        payment.save_record()

        # Filter payments by date
        filtered_payments = PayCredit.filter_payments_by_date("2025-04-01", "2025-04-30")
        print(f"Filtered payments in April 2025: {filtered_payments}")

        # Print the total amount paid
        total_paid = PayCredit.sum_amount_paid()
        print(f"Total amount paid: {total_paid:.2f}")
    except Exception as e:
        print(f"An error occurred during testing: {e}")