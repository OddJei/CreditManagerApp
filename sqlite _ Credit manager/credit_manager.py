from datetime import datetime
from db_utility import DBUtility as db
import sqlite3

class Credit:
    def __init__(self, customer_id, amount_credited, date_credited=None):
        self.customer_id = customer_id
        self.date_credited = date_credited if date_credited else datetime.now().strftime("%Y-%m-%d")  # Default to current date
        self.amount_credited = amount_credited
        self.create_table()
        self.validate_customer()

    def create_table(self):
        # Create the Credits table if it doesn't exist
        schema = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            date_credited TEXT TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            amount_credited REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        '''
        db.create_table("Credits", schema)

    def validate_customer(self):
        # Ensure the customer exists in the Customers table
        existing_customers = db.fetch_unique_values("customer_id", "Customers")
        if self.customer_id not in existing_customers:
            raise ValueError(f"Customer ID {self.customer_id} does not exist in the system.")

    def save_record(self):
        # Save credit record to the Credits table
        columns = "customer_id, date_credited, amount_credited"
        values = (self.customer_id, self.date_credited, self.amount_credited)
        db.save_record("Credits", columns, values)

    @staticmethod
    def filter_credits_by_date(start_date, end_date):
        """
        Fetch credits within a specific date range.

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
                    SELECT customer_id, date_credited, amount_credited
                    FROM Credits
                    WHERE date_credited BETWEEN ? AND ?
                '''
                cursor.execute(query, (start_date, end_date))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error filtering credits by date: {e}")
            return []

    @staticmethod
    def sum_amount_credited():
        """
        Fetch the total credited amount from the database.

        Returns:
        - Total credited amount as a float.
        """
        try:
            with sqlite3.connect(db.DB_NAME) as connection:
                cursor = connection.cursor()
                query = '''
                    SELECT SUM(amount_credited)
                    FROM Credits
                '''
                cursor.execute(query)
                return cursor.fetchone()[0] or 0.0
        except sqlite3.Error as e:
            print(f"Error summing credited amounts: {e}")
            return 0.0


# Test Code
if __name__ == "__main__":
    try:
        # Create a credit record
        credit = Credit("2025041201", 100.00)  # Customer ID and credited amount
        credit.save_record()

        # Filter credits by date
        filtered_credits = Credit.filter_credits_by_date("2025-04-01", "2025-04-30")
        print(f"Filtered credits in April 2025: {filtered_credits}")

        # Print the total amount credited
        total_credited = Credit.sum_amount_credited()
        print(f"Total amount credited: {total_credited:.2f}")
    except Exception as e:
        print(f"An error occurred during testing: {e}")